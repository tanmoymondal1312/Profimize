from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify


CATEGORIES = [
    {"name": "Digital Marketing", "slug": "digital-marketing", "description": "Tips and strategies for growing your business online."},
    {"name": "Web Development", "slug": "web-development", "description": "Insights on building fast, beautiful, and scalable websites."},
    {"name": "SEO", "slug": "seo", "description": "Search engine optimisation strategies to rank higher and drive organic traffic."},
]

POSTS = [
    {
        "title": "10 Digital Marketing Strategies That Actually Work in 2024",
        "slug": "10-digital-marketing-strategies-2024",
        "category_slug": "digital-marketing",
        "excerpt": "Stop wasting budget on tactics that don't move the needle. Here are 10 proven digital marketing strategies driving real results for businesses in 2024.",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "body": (
            "<h2>Why Most Marketing Fails</h2>"
            "<p>The biggest mistake businesses make is treating digital marketing as a checklist rather than a strategy. "
            "Posting on social media every day means nothing if you're talking to the wrong audience with the wrong message.</p>"
            "<h2>1. Build a Content Engine First</h2>"
            "<p>Before running a single ad, invest in content that answers your target customer's most pressing questions. "
            "This earns trust, builds organic traffic, and gives you material to fuel every other channel.</p>"
            "<h2>2. SEO Is a Long-Term Asset</h2>"
            "<p>Paid ads stop the moment you stop spending. A well-optimised page can deliver qualified traffic for years. "
            "Invest in keyword research, on-page SEO, and authoritative backlinks from day one.</p>"
            "<h2>3. Social Proof Converts</h2>"
            "<p>Case studies, testimonials, and before/after results are the most persuasive content you can publish. "
            "Make them central to your homepage, landing pages, and social profiles.</p>"
            "<h2>4. Email Remains King</h2>"
            "<p>With an average ROI of $36 for every $1 spent, email marketing outperforms every other channel. "
            "Build your list from day one and nurture it with genuine value.</p>"
            "<h2>5. Video First on Social</h2>"
            "<p>Platforms reward video content with organic reach. A 60-second reel explaining your service will "
            "consistently outperform a static image post.</p>"
        ),
        "meta_title": "10 Digital Marketing Strategies That Work in 2024 | Profimize",
        "meta_description": "Discover 10 proven digital marketing strategies driving real results in 2024 — from content and SEO to social media and email.",
    },
    {
        "title": "Why Your Website Is Costing You Customers (And How to Fix It)",
        "slug": "why-your-website-is-costing-you-customers",
        "category_slug": "web-development",
        "excerpt": "A slow, outdated, or confusing website doesn't just lose visitors — it actively drives potential customers to your competitors. Here's how to diagnose and fix the most common issues.",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "body": (
            "<h2>The Hidden Cost of a Bad Website</h2>"
            "<p>53% of mobile users abandon a site that takes longer than 3 seconds to load. If your site is slow, "
            "you're not just losing traffic — you're handing customers directly to your competitors.</p>"
            "<h2>Problem 1: Slow Load Speed</h2>"
            "<p>The most common culprit is unoptimised images. A single hero image over 2MB can add 2-3 seconds to "
            "your load time. Convert images to WebP format and lazy-load anything below the fold.</p>"
            "<h2>Problem 2: No Clear Call to Action</h2>"
            "<p>Every page on your site should have one primary action you want visitors to take. If your homepage "
            "has five different CTAs competing for attention, visitors will choose none of them.</p>"
            "<h2>Problem 3: Not Mobile-First</h2>"
            "<p>Over 60% of web traffic comes from mobile devices. If your site isn't designed mobile-first, "
            "you're delivering a broken experience to the majority of your visitors.</p>"
            "<h2>Problem 4: No Social Proof Above the Fold</h2>"
            "<p>Visitors decide within 5 seconds whether to trust your site. Client logos, testimonials, "
            "and results data need to appear before the user has to scroll.</p>"
            "<h2>The Fix</h2>"
            "<p>Run a free Google PageSpeed Insights audit, fix the top three issues, and test your homepage "
            "with a 5-second test on UsabilityHub. Small improvements compound into significant revenue gains.</p>"
        ),
        "meta_title": "Why Your Website Is Losing Customers | Profimize",
        "meta_description": "A slow or confusing website drives customers to competitors. Learn how to identify and fix the most damaging web design mistakes.",
    },
    {
        "title": "The Complete Beginner's Guide to SEO in Bangladesh",
        "slug": "beginners-guide-seo-bangladesh",
        "category_slug": "seo",
        "excerpt": "SEO doesn't have to be complicated. This beginner-friendly guide explains everything you need to know to start ranking your Bangladeshi business on Google — step by step.",
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "body": (
            "<h2>What Is SEO and Why Does It Matter?</h2>"
            "<p>Search Engine Optimisation (SEO) is the process of improving your website so it appears higher in "
            "Google search results when people search for your products or services. The higher you rank, the more "
            "free, targeted traffic you receive.</p>"
            "<h2>Step 1: Keyword Research</h2>"
            "<p>Start by identifying what your potential customers are actually searching for. Use free tools like "
            "Google Keyword Planner or Ubersuggest to find keywords with decent search volume and manageable competition. "
            "In Bangladesh, focus on Bengali and English keyword variations.</p>"
            "<h2>Step 2: On-Page Optimisation</h2>"
            "<p>Every page should target one primary keyword. Include it in your page title, H1 heading, first paragraph, "
            "and at least one subheading. Keep your meta description under 155 characters and make it compelling enough "
            "to earn the click.</p>"
            "<h2>Step 3: Technical SEO Foundations</h2>"
            "<p>Ensure your site loads in under 3 seconds, uses HTTPS, has a valid sitemap submitted to Google Search "
            "Console, and has no broken links. These fundamentals are non-negotiable.</p>"
            "<h2>Step 4: Local SEO</h2>"
            "<p>If you serve customers in Dhaka, Chittagong, or any specific city, create and optimise your Google "
            "Business Profile. Add your business address, phone number, opening hours, and photos. "
            "Consistent NAP (Name, Address, Phone) across the web is essential.</p>"
            "<h2>Step 5: Build Authority with Content</h2>"
            "<p>Publish one high-quality blog post per week that answers a question your target customer is asking. "
            "Over time, this builds topical authority and earns backlinks — the two most important ranking factors.</p>"
        ),
        "meta_title": "Beginner's Guide to SEO in Bangladesh | Profimize",
        "meta_description": "Learn SEO from scratch with this complete beginner's guide — keyword research, on-page optimisation, local SEO, and content strategy for Bangladeshi businesses.",
    },
]


def seed_posts(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    Post = apps.get_model("blog", "Post")

    cat_map = {}
    for cat_data in CATEGORIES:
        cat, _ = Category.objects.get_or_create(
            slug=cat_data["slug"],
            defaults={"name": cat_data["name"], "description": cat_data["description"]},
        )
        cat_map[cat_data["slug"]] = cat

    for p in POSTS:
        if not Post.objects.filter(slug=p["slug"]).exists():
            Post.objects.create(
                title=p["title"],
                slug=p["slug"],
                excerpt=p["excerpt"],
                body=p["body"],
                youtube_url=p["youtube_url"],
                category=cat_map.get(p["category_slug"]),
                status="published",
                published_at=timezone.now(),
                meta_title=p.get("meta_title", ""),
                meta_description=p.get("meta_description", ""),
            )


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_posts, reverse_seed),
    ]
