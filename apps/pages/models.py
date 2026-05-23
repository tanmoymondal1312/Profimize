from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=100, default="Profimize")
    tagline = models.CharField(max_length=200, default="Grow your business by professional digital marketing")
    phone = models.CharField(max_length=30, default="+8801745274403")
    email = models.EmailField(default="souravmondalcode@gmail.com")
    address = models.CharField(max_length=200, default="Mirpur-1, Dhaka, Bangladesh")
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    default_og_image = models.ImageField(upload_to="site/", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    what_we_offer = models.TextField(blank=True, help_text="One item per line")
    our_process = models.TextField(blank=True, help_text="One step per line")
    meta_description = models.CharField(max_length=160, blank=True)
    icon_name = models.CharField(max_length=60, help_text="Lucide icon key, e.g. 'code'")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("pages:service_detail", kwargs={"slug": self.slug})


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("Web Development", "Web Development"),
        ("Content Creation", "Content Creation"),
        ("SEO", "SEO"),
        ("Video Editing", "Video Editing"),
        ("Marketing", "Marketing"),
    ]
    FILTER_CHOICES = [
        ("development", "Development"),
        ("creative", "Creative"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, max_length=220)
    url = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    filter_group = models.CharField(max_length=20, choices=FILTER_CHOICES)
    image = models.ImageField(upload_to="projects/", blank=True)
    full_description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, blank=True, help_text="Comma-separated")
    client_name = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=10, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("pages:project_detail", kwargs={"slug": self.slug})


class Testimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Stat(models.Model):
    value = models.CharField(max_length=20)
    label = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.value} — {self.label}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.name} — {self.subject}"


class SiteVisit(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}: {self.count} visits"
