import django.db.models.deletion
import django_ckeditor_5.fields
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"verbose_name_plural": "Categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(db_index=True, max_length=220, unique=True)),
                ("excerpt", models.CharField(help_text="Brief summary shown in cards (≤300 chars)", max_length=300)),
                ("body", django_ckeditor_5.fields.CKEditor5Field(config_name="default")),
                ("thumbnail", models.ImageField(blank=True, upload_to="blog/thumbs/")),
                ("youtube_url", models.URLField(blank=True, help_text="Leave image blank and paste a YouTube URL to use a video thumbnail")),
                ("status", models.CharField(choices=[("draft", "Draft"), ("published", "Published")], db_index=True, default="draft", max_length=12)),
                ("is_featured", models.BooleanField(default=False)),
                ("meta_title", models.CharField(blank=True, max_length=70)),
                ("meta_description", models.CharField(blank=True, max_length=160)),
                ("og_image", models.ImageField(blank=True, upload_to="blog/og/")),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("reading_time", models.PositiveIntegerField(default=1, help_text="Auto-computed minutes")),
                ("published_at", models.DateTimeField(db_index=True, null=True, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posts", to="blog.category")),
                ("author", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posts", to=settings.AUTH_USER_MODEL)),
                ("tags", taggit.managers.TaggableManager(blank=True, help_text="A comma-separated list of tags.", through="taggit.TaggedItem", to="taggit.Tag", verbose_name="Tags")),
            ],
            options={"ordering": ["-published_at"]},
        ),
    ]
