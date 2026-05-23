from django.db import migrations
from django.utils.text import slugify


SERVICE_RICH = {
    "web-development": {
        "long_description": (
            "At Profimize, we don't just build websites — we engineer digital experiences that convert visitors into customers. "
            "Every project starts with a deep understanding of your business goals, target audience, and competitive landscape. "
            "We craft pixel-perfect designs and back them with clean, performant code optimised for speed and search engines.\n\n"
            "Whether you need a landing page that sells, a feature-rich e-commerce store, or a complex web application, "
            "our team has the expertise to deliver. We use modern frameworks and best practices to ensure your site is "
            "secure, scalable, and future-proof."
        ),
        "what_we_offer": (
            "Custom website design & development\n"
            "Responsive, mobile-first layouts\n"
            "E-commerce development (WooCommerce, Shopify, custom)\n"
            "Web application development\n"
            "Landing page design & A/B optimisation\n"
            "Website speed optimisation & Core Web Vitals\n"
            "CMS integration (WordPress, Django, headless)\n"
            "Ongoing maintenance & support"
        ),
        "our_process": (
            "Discovery & goal-setting — we audit your current site and define measurable objectives\n"
            "UX wireframing — low-fidelity blueprints reviewed and approved before design begins\n"
            "Visual design — high-fidelity mockups in your brand palette with interactive prototypes\n"
            "Development & QA — clean code, cross-browser testing, accessibility audit\n"
            "Launch & hand-over — deployment, DNS setup, analytics, and team training"
        ),
        "meta_description": "Custom web development by Profimize — fast, responsive, SEO-ready websites and web apps designed to convert visitors into paying customers.",
    },
    "mobile-app-development": {
        "long_description": (
            "Mobile is where your customers spend most of their time. Profimize builds native and cross-platform mobile apps "
            "that deliver a seamless experience on both iOS and Android. We focus on intuitive UI, blazing performance, and "
            "rock-solid backend integration so your app works flawlessly from day one.\n\n"
            "From MVP to enterprise-grade product, we guide you through every stage — ideation, design, development, "
            "App Store submission, and post-launch iterations driven by real user feedback."
        ),
        "what_we_offer": (
            "iOS & Android native app development\n"
            "Cross-platform apps (React Native, Flutter)\n"
            "UI/UX design for mobile\n"
            "API & backend integration\n"
            "Push notifications & real-time features\n"
            "App Store & Google Play submission\n"
            "Performance monitoring & crash analytics\n"
            "Ongoing updates & feature development"
        ),
        "our_process": (
            "Requirements & feature scoping — translate your idea into a prioritised feature list\n"
            "UI/UX prototyping — clickable prototypes tested with real users before a line of code is written\n"
            "Agile development sprints — two-week cycles with demos and feedback at every milestone\n"
            "QA & device testing — tested on 20+ device/OS combinations\n"
            "Store submission & launch — optimised metadata, screenshots, and ASO strategy"
        ),
        "meta_description": "Profimize builds native and cross-platform mobile apps for iOS and Android — from concept and design to App Store launch and beyond.",
    },
    "social-media-marketing": {
        "long_description": (
            "Social media is the fastest way to put your brand in front of thousands of potential customers — if done right. "
            "Profimize creates data-driven social media strategies that grow your following, spark genuine engagement, and "
            "turn scrollers into buyers. We manage everything from content creation and scheduling to paid ad campaigns and reporting.\n\n"
            "Our team stays ahead of every algorithm change so your content always reaches the right people at the right time."
        ),
        "what_we_offer": (
            "Full-service social media management (Facebook, Instagram, LinkedIn, YouTube)\n"
            "Content calendar creation & scheduling\n"
            "Professional graphic design & copywriting\n"
            "Facebook & Instagram Ads — campaign setup, targeting, and optimisation\n"
            "Community management & comment moderation\n"
            "Influencer outreach & collaboration\n"
            "Monthly analytics & performance reports\n"
            "Competitor analysis & benchmarking"
        ),
        "our_process": (
            "Audit & strategy — deep dive into your current presence and define content pillars\n"
            "Content production — graphics, captions, and video clips created to platform specs\n"
            "Scheduling & posting — consistent publishing at peak engagement times\n"
            "Paid campaign management — A/B tested ads optimised for your KPIs\n"
            "Monthly reporting & strategy refinement — transparent data, clear next steps"
        ),
        "meta_description": "Profimize manages your social media marketing — content, ads, and community management — to grow your audience and drive real business results.",
    },
    "seo": {
        "long_description": (
            "Ranking on page one of Google is no longer optional — it's essential. Profimize delivers comprehensive SEO "
            "strategies that combine technical excellence, authoritative content, and high-quality backlinks to push your "
            "site to the top and keep it there.\n\n"
            "We don't chase short-term tricks. Every strategy we build is designed to deliver sustainable organic growth "
            "that compounds over time, turning your website into your best-performing sales channel."
        ),
        "what_we_offer": (
            "Technical SEO audit & implementation\n"
            "Keyword research & content strategy\n"
            "On-page optimisation (titles, meta, schema, internal links)\n"
            "Content writing & blog strategy\n"
            "Link building & digital PR\n"
            "Local SEO (Google Business Profile optimisation)\n"
            "Core Web Vitals & page speed optimisation\n"
            "Monthly rank tracking & reporting"
        ),
        "our_process": (
            "SEO audit — crawl your site, identify technical issues and quick wins\n"
            "Keyword mapping — match the right keywords to the right pages\n"
            "On-page implementation — optimise every element Google uses to rank pages\n"
            "Content & links — publish authoritative content and earn high-DR backlinks\n"
            "Monitor & iterate — monthly reports with clear rankings, traffic, and revenue impact"
        ),
        "meta_description": "Profimize SEO services — technical SEO, content strategy, and link building that rank your site on Google and turn organic traffic into revenue.",
    },
    "video-production": {
        "long_description": (
            "Video is the highest-converting content format online. Profimize produces professional promotional videos, "
            "YouTube content, social media reels, and corporate films that capture attention and communicate your brand story "
            "in a way no other medium can.\n\n"
            "From scripting and storyboarding to filming, editing, colour grading, and music licensing, we handle the entire "
            "production pipeline so you can focus on running your business."
        ),
        "what_we_offer": (
            "Promotional & brand films\n"
            "YouTube video production & channel strategy\n"
            "Instagram & Facebook Reels / TikTok content\n"
            "Product demonstration videos\n"
            "Testimonial & case study videos\n"
            "Scriptwriting & storyboarding\n"
            "Professional editing, colour grading & sound design\n"
            "Motion graphics & animated explainer videos"
        ),
        "our_process": (
            "Brief & creative strategy — understand your message, audience, and distribution platform\n"
            "Scripting & storyboarding — every second planned before the camera rolls\n"
            "Production — filming with professional equipment or remote video collection\n"
            "Post-production — editing, colour, sound, subtitles, and motion graphics\n"
            "Delivery & distribution strategy — optimised formats for every platform"
        ),
        "meta_description": "Professional video production by Profimize — promotional films, YouTube content, reels, and explainers that captivate audiences and grow your brand.",
    },
    "content-marketing": {
        "long_description": (
            "Content is the foundation of every successful digital marketing strategy. Profimize creates strategic blog posts, "
            "infographics, email sequences, and long-form guides that educate your audience, establish your authority, and "
            "fuel every stage of the marketing funnel from awareness to conversion.\n\n"
            "Every piece of content we create is researched, SEO-optimised, and tailored to your brand voice — so it "
            "attracts the right visitors and turns them into leads."
        ),
        "what_we_offer": (
            "Blog strategy & SEO content writing\n"
            "Long-form guides & whitepapers\n"
            "Email marketing sequences & newsletters\n"
            "Infographic design & data visualisation\n"
            "Social media copywriting\n"
            "Case studies & success stories\n"
            "Content audits & repurposing\n"
            "Editorial calendar management"
        ),
        "our_process": (
            "Content audit — identify what you already have and what gaps need filling\n"
            "Keyword & topic research — find content opportunities your competitors are missing\n"
            "Content production — expert writing, design, and optimisation for search and conversion\n"
            "Publishing & distribution — post across channels and promote via email and social\n"
            "Performance tracking — measure traffic, engagement, leads, and update content quarterly"
        ),
        "meta_description": "Profimize content marketing — SEO blog posts, email sequences, infographics, and guides that build your authority and drive qualified leads.",
    },
}

PROJECT_RICH = [
    {
        "title": "Sahaj Shekha — EdTech Platform",
        "slug": "sahaj-shekha-edtech-platform",
        "full_description": (
            "Sahaj Shekha is a full-featured online learning platform built for Bangladeshi students and educators. "
            "Profimize designed and developed the entire platform from scratch — including a custom course management system, "
            "video lesson delivery, quiz engine, and payment gateway integration.\n\n"
            "The result is a lightning-fast, mobile-first web app that has served thousands of learners since launch, "
            "with consistently high satisfaction scores and a sub-2-second page load time on mobile."
        ),
        "tech_stack": "Django, PostgreSQL, Redis, Celery, Tailwind CSS, AWS S3",
        "client_name": "Sahaj Shekha Ltd.",
        "year": "2023",
    },
    {
        "title": "Rainbow Tools — SaaS Dashboard",
        "slug": "rainbow-tools-saas-dashboard",
        "full_description": (
            "Rainbow Tools is a multi-tenant SaaS platform providing digital marketing utilities for agencies. "
            "Profimize built the complete product — from brand identity and landing page to the full-stack web application "
            "with subscription billing, role-based access control, and a real-time analytics dashboard.\n\n"
            "The platform now handles thousands of API requests per day and has maintained 99.9% uptime since launch."
        ),
        "tech_stack": "Django REST Framework, React, Stripe, PostgreSQL, Docker, Nginx",
        "client_name": "Rainbow Tools Inc.",
        "year": "2024",
    },
    {
        "title": "Dhaka Foodies — Food Blog",
        "slug": "dhaka-foodies-food-blog",
        "full_description": (
            "Dhaka Foodies is a content-first food blog targeting food lovers across Bangladesh. "
            "Profimize built the site on a headless CMS, designed the visual identity, and created an ongoing "
            "content marketing strategy that grew the blog from zero to 15,000 monthly readers in four months.\n\n"
            "The project also included a custom recipe schema implementation that earned rich snippets on Google, "
            "dramatically boosting organic CTR."
        ),
        "tech_stack": "WordPress, SEO, Content Marketing, Google Search Console",
        "client_name": "Dhaka Foodies",
        "year": "2023",
    },
    {
        "title": "TechBD YouTube Channel",
        "slug": "techbd-youtube-channel",
        "full_description": (
            "TechBD is a Bangladeshi tech education YouTube channel. Profimize managed the full video production pipeline — "
            "scripting, filming, editing, thumbnail design — and executed a YouTube SEO strategy that grew the channel "
            "from 800 to over 12,000 subscribers in six months.\n\n"
            "Average view duration increased by 40% after we restructured video formats based on audience retention analytics."
        ),
        "tech_stack": "Adobe Premiere Pro, After Effects, YouTube Analytics, Canva",
        "client_name": "TechBD Media",
        "year": "2023",
    },
    {
        "title": "Local Startup SEO Campaign",
        "slug": "local-startup-seo-campaign",
        "full_description": (
            "A Dhaka-based B2B startup hired Profimize to grow their organic presence from virtually zero. "
            "We conducted a full technical SEO audit, rebuilt their site architecture, wrote 24 long-form blog articles, "
            "and executed a targeted link-building campaign.\n\n"
            "Within 8 months the site ranked on page one for 37 target keywords and organic sessions grew by 680%, "
            "contributing directly to a 3x increase in qualified inbound leads."
        ),
        "tech_stack": "Ahrefs, SEMrush, Google Search Console, WordPress",
        "client_name": "Confidential (B2B SaaS)",
        "year": "2024",
    },
    {
        "title": "Brand Identity & Social Kit",
        "slug": "brand-identity-social-kit",
        "full_description": (
            "A retail fashion brand approached Profimize for a complete brand overhaul. We created a new logo, "
            "colour system, typography guide, and a full social media kit including 60+ post templates for "
            "Instagram, Facebook, and LinkedIn.\n\n"
            "The brand refresh led to a 45% increase in social media engagement in the first month and positioned "
            "the brand as a premium choice in their market segment."
        ),
        "tech_stack": "Adobe Illustrator, Figma, Canva, Social Media Strategy",
        "client_name": "Fashion Retail Brand",
        "year": "2024",
    },
]


def seed_rich_content(apps, schema_editor):
    Service = apps.get_model("pages", "Service")
    Project = apps.get_model("pages", "Project")

    for slug, data in SERVICE_RICH.items():
        Service.objects.filter(slug=slug).update(**data)

    for p_data in PROJECT_RICH:
        title = p_data["title"]
        slug = p_data["slug"]
        update_data = {k: v for k, v in p_data.items() if k not in ("title", "slug")}
        Project.objects.filter(title=title).update(slug=slug, **update_data)


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_add_fields_and_sitevisit"),
    ]

    operations = [
        migrations.RunPython(seed_rich_content, reverse_seed),
    ]
