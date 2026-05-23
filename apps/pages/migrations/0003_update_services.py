from django.db import migrations


def update_services(apps, schema_editor):
    Service = apps.get_model("pages", "Service")

    # Remove Mobile App Marketing
    Service.objects.filter(slug="mobile-app-marketing").delete()

    # Shift services at order >=2 up by 1 to make room for the new card at position 2
    for svc in Service.objects.filter(order__gte=2).order_by("-order"):
        svc.order += 1
        svc.save()

    # Add Mobile App Development right after Web Development
    Service.objects.get_or_create(
        slug="mobile-app-development",
        defaults={
            "title": "Mobile App Development",
            "description": "We design and build native and cross-platform mobile apps for iOS and Android — from intuitive UI to rock-solid backend integration — that users actually love to use.",
            "icon_name": "smartphone",
            "order": 2,
            "is_active": True,
        },
    )


def reverse_update_services(apps, schema_editor):
    Service = apps.get_model("pages", "Service")
    Service.objects.filter(slug="mobile-app-development").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_seed"),
    ]

    operations = [
        migrations.RunPython(update_services, reverse_update_services),
    ]
