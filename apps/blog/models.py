import re
import logging
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

logger = logging.getLogger(__name__)
User = get_user_model()

_YT_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?.*?v=|shorts/|embed/)|youtu\.be/)([A-Za-z0-9_-]{11})"
)


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:category", kwargs={"slug": self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status="published", published_at__lte=timezone.now())
            .order_by("-published_at")
        )


class Post(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220, db_index=True)
    excerpt = models.CharField(max_length=300, help_text="Brief summary shown in cards (≤300 chars)")
    body = CKEditor5Field(config_name="default")

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts")
    tags = TaggableManager(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")

    thumbnail = models.ImageField(upload_to="blog/thumbs/", blank=True)
    youtube_url = models.URLField(blank=True, help_text="Leave image blank and paste a YouTube URL to use a video thumbnail")

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft", db_index=True)
    is_featured = models.BooleanField(default=False)

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="blog/og/", blank=True)

    view_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=1, help_text="Auto-computed minutes")

    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    # --- helpers ---

    @property
    def youtube_id(self):
        if not self.youtube_url:
            return ""
        m = _YT_RE.search(self.youtube_url)
        return m.group(1) if m else ""

    @property
    def has_video(self):
        return bool(self.youtube_url)

    @property
    def thumb_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        yt_id = self.youtube_id
        if yt_id:
            return f"https://i.ytimg.com/vi/{yt_id}/hqdefault.jpg"
        return "/static/img/og-default.jpg"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:detail", kwargs={"slug": self.slug})

    # --- save logic ---

    def _compress_image(self, field):
        """Convert uploaded image to WebP ≤1600px. Safe — never raises."""
        try:
            import io
            from PIL import Image
            from django.core.files.base import ContentFile

            img = Image.open(field)
            img = img.convert("RGB")
            max_side = 1600
            w, h = img.size
            if max(w, h) > max_side:
                ratio = max_side / max(w, h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="WEBP", quality=80, optimize=True)
            buf.seek(0)
            name = field.name.rsplit(".", 1)[0] + ".webp"
            field.save(name, ContentFile(buf.read()), save=False)
        except Exception:
            logger.warning("Image compression failed for post '%s'; keeping original.", self.title)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.thumbnail and not self.youtube_url:
            raise ValidationError("A post must have either a thumbnail image or a YouTube URL.")

    def save(self, *args, **kwargs):
        # Auto slug
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug

        # Reading time
        import re as _re
        words = len(_re.findall(r"\w+", self.body or ""))
        self.reading_time = max(1, words // 200)

        # Published_at timestamp
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        # Compress images (only on new uploads)
        try:
            old = Post.objects.get(pk=self.pk)
        except Post.DoesNotExist:
            old = None

        super().save(*args, **kwargs)

        # Compress after save so the file exists on disk
        compress_thumb = self.thumbnail and (old is None or old.thumbnail != self.thumbnail)
        compress_og = self.og_image and (old is None or old.og_image != self.og_image)
        if compress_thumb:
            self._compress_image(self.thumbnail)
            Post.objects.filter(pk=self.pk).update(thumbnail=self.thumbnail.name)
        if compress_og:
            self._compress_image(self.og_image)
            Post.objects.filter(pk=self.pk).update(og_image=self.og_image.name)
