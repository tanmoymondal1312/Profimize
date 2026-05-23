from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from config.sitemaps import StaticViewSitemap
from apps.blog.sitemaps import PostSitemap, CategorySitemap


sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "categories": CategorySitemap,
}

urlpatterns = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("manifest.json", TemplateView.as_view(template_name="manifest.json", content_type="application/json")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("blog/", include("apps.blog.urls", namespace="blog")),
    path("", include("apps.pages.urls", namespace="pages")),
]

handler404 = "apps.pages.views.custom_404"
handler500 = "apps.pages.views.custom_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
