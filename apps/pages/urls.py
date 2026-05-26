from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    # RESTORE: uncomment when portfolio is re-enabled (~1 year from 2026-05-26)
    # path("portfolio/<slug:slug>/", views.project_detail, name="project_detail"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("faq/", views.faq, name="faq"),
    path("career/", views.career, name="career"),
]
