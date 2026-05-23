from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("brand_name", models.CharField(default="Profimize", max_length=100)),
                ("tagline", models.CharField(default="Grow your business by professional digital marketing", max_length=200)),
                ("phone", models.CharField(default="+8801745274403", max_length=30)),
                ("email", models.EmailField(default="souravmondalcode@gmail.com", max_length=254)),
                ("address", models.CharField(default="Mirpur-1, Dhaka, Bangladesh", max_length=200)),
                ("facebook", models.URLField(blank=True)),
                ("twitter", models.URLField(blank=True)),
                ("instagram", models.URLField(blank=True)),
                ("linkedin", models.URLField(blank=True)),
                ("youtube", models.URLField(blank=True)),
                ("default_og_image", models.ImageField(blank=True, upload_to="site/")),
            ],
            options={"verbose_name": "Site Settings", "verbose_name_plural": "Site Settings"},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("icon_name", models.CharField(help_text="Lucide icon key, e.g. 'code'", max_length=60)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order"], "verbose_name": "Service"},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("url", models.URLField(blank=True)),
                ("category", models.CharField(choices=[("Web Development", "Web Development"), ("Content Creation", "Content Creation"), ("SEO", "SEO"), ("Video Editing", "Video Editing"), ("Marketing", "Marketing")], max_length=50)),
                ("filter_group", models.CharField(choices=[("development", "Development"), ("creative", "Creative")], max_length=20)),
                ("image", models.ImageField(blank=True, upload_to="projects/")),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quote", models.TextField()),
                ("name", models.CharField(max_length=100)),
                ("role", models.CharField(max_length=100)),
                ("avatar", models.ImageField(blank=True, upload_to="avatars/")),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Stat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=20)),
                ("label", models.CharField(max_length=80)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Contact Message"},
        ),
    ]
