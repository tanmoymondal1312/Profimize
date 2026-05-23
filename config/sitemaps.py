from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return [
            "pages:home",
            "pages:about",
            "pages:services",
            "pages:contact",
            "pages:faq",
            "pages:career",
            "pages:privacy",
            "blog:list",
        ]

    def location(self, item):
        return reverse(item)
