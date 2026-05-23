from django.db import migrations


SERVICES = [
    {
        "title": "Web Development",
        "slug": "web-development",
        "description": "We build fast, responsive, and conversion-optimised websites and web applications tailored to your brand — from landing pages to complex e-commerce platforms.",
        "icon_name": "code",
        "order": 1,
    },
    {
        "title": "Mobile App Development",
        "slug": "mobile-app-development",
        "description": "We design and build native and cross-platform mobile apps for iOS and Android — from intuitive UI to rock-solid backend integration — that users actually love to use.",
        "icon_name": "smartphone",
        "order": 2,
    },
    {
        "title": "Social Media Marketing",
        "slug": "social-media-marketing",
        "description": "Grow your audience and drive real engagement across Facebook, Instagram, LinkedIn, and YouTube with data-driven content strategies and targeted ad campaigns.",
        "icon_name": "share-2",
        "order": 3,
    },
    {
        "title": "Search Engine Optimisation",
        "slug": "seo",
        "description": "Rank higher on Google with our proven on-page, off-page, and technical SEO strategies. We turn organic traffic into qualified leads and long-term revenue.",
        "icon_name": "search",
        "order": 4,
    },
    {
        "title": "Video Production & Editing",
        "slug": "video-production",
        "description": "From concept to final cut — we produce high-quality promotional videos, reels, and YouTube content that captivate viewers and communicate your brand story.",
        "icon_name": "video",
        "order": 5,
    },
    {
        "title": "Content Marketing",
        "slug": "content-marketing",
        "description": "Strategic blog posts, infographics, and copy that educate your audience, build authority, and fuel every stage of the marketing funnel.",
        "icon_name": "megaphone",
        "order": 6,
    },
]

PROJECTS = [
    {
        "title": "Sahaj Shekha — EdTech Platform",
        "url": "https://sahajshekha.com",
        "category": "Web Development",
        "filter_group": "development",
        "order": 1,
    },
    {
        "title": "Rainbow Tools — SaaS Dashboard",
        "url": "https://rainbowtools.app",
        "category": "Web Development",
        "filter_group": "development",
        "order": 2,
    },
    {
        "title": "Dhaka Foodies — Food Blog",
        "url": "#",
        "category": "Content Creation",
        "filter_group": "creative",
        "order": 3,
    },
    {
        "title": "TechBD YouTube Channel",
        "url": "#",
        "category": "Video Editing",
        "filter_group": "creative",
        "order": 4,
    },
    {
        "title": "Local Startup SEO Campaign",
        "url": "#",
        "category": "SEO",
        "filter_group": "development",
        "order": 5,
    },
    {
        "title": "Brand Identity & Social Kit",
        "url": "#",
        "category": "Marketing",
        "filter_group": "creative",
        "order": 6,
    },
]

TESTIMONIALS = [
    {
        "quote": "Profimize completely transformed our online presence. Within three months our organic traffic doubled and our enquiry rate went through the roof. Sourav and the team really understand digital marketing.",
        "name": "Rafiqul Islam",
        "role": "CEO, Sahaj Shekha",
        "order": 1,
    },
    {
        "quote": "The website they built for us is fast, beautiful, and ranks on the first page of Google. The ROI has been phenomenal. I'd recommend Profimize to any business that's serious about growth.",
        "name": "Nasrin Akter",
        "role": "Founder, DhakaStyle Boutique",
        "order": 2,
    },
    {
        "quote": "Professional, creative, and always on time. Our YouTube channel grew from zero to 10k subscribers in six months thanks to their video strategy. Absolutely outstanding service.",
        "name": "Mehedi Hasan",
        "role": "Content Creator & Entrepreneur",
        "order": 3,
    },
]

STATS = [
    {"value": "50+", "label": "Happy Clients", "order": 1},
    {"value": "100+", "label": "Projects Delivered", "order": 2},
    {"value": "3+", "label": "Years of Experience", "order": 3},
    {"value": "100%", "label": "Client Satisfaction", "order": 4},
]

SITE_SETTINGS = {
    "brand_name": "Profimize",
    "tagline": "Grow your business by professional digital marketing",
    "phone": "+8801745274403",
    "email": "souravmondalcode@gmail.com",
    "address": "Mirpur-1, Dhaka, Bangladesh",
    "facebook": "https://facebook.com/profimize",
    "twitter": "https://twitter.com/profimize",
    "instagram": "https://instagram.com/profimize",
    "linkedin": "https://linkedin.com/company/profimize",
    "youtube": "https://youtube.com/@profimize",
}


def seed_data(apps, schema_editor):
    SiteSettings = apps.get_model("pages", "SiteSettings")
    Service = apps.get_model("pages", "Service")
    Project = apps.get_model("pages", "Project")
    Testimonial = apps.get_model("pages", "Testimonial")
    Stat = apps.get_model("pages", "Stat")

    SiteSettings.objects.get_or_create(pk=1, defaults=SITE_SETTINGS)

    for s in SERVICES:
        Service.objects.get_or_create(slug=s["slug"], defaults=s)

    for p in PROJECTS:
        Project.objects.get_or_create(title=p["title"], defaults=p)

    for t in TESTIMONIALS:
        Testimonial.objects.get_or_create(name=t["name"], defaults=t)

    for st in STATS:
        Stat.objects.get_or_create(label=st["label"], defaults=st)


def unseed_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
