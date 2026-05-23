from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_update_services"),
    ]

    operations = [
        # Service new fields
        migrations.AddField(
            model_name="service",
            name="long_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="service",
            name="what_we_offer",
            field=models.TextField(blank=True, help_text="One item per line"),
        ),
        migrations.AddField(
            model_name="service",
            name="our_process",
            field=models.TextField(blank=True, help_text="One step per line"),
        ),
        migrations.AddField(
            model_name="service",
            name="meta_description",
            field=models.CharField(blank=True, max_length=160),
        ),
        # Project new fields
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, max_length=220, unique=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="full_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="tech_stack",
            field=models.CharField(blank=True, max_length=300, help_text="Comma-separated"),
        ),
        migrations.AddField(
            model_name="project",
            name="client_name",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="project",
            name="year",
            field=models.CharField(blank=True, max_length=10),
        ),
        # SiteVisit model
        migrations.CreateModel(
            name="SiteVisit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
