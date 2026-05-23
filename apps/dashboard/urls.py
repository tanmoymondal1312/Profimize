from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("login/", views.dashboard_login, name="login"),
    path("logout/", views.dashboard_logout, name="logout"),

    # Messages
    path("messages/", views.messages_list, name="messages"),
    path("messages/<int:pk>/read/", views.message_read, name="message_read"),
    path("messages/<int:pk>/delete/", views.message_delete, name="message_delete"),

    # Services
    path("services/", views.services_list, name="services"),
    path("services/add/", views.service_add, name="service_add"),
    path("services/<int:pk>/edit/", views.service_edit, name="service_edit"),
    path("services/<int:pk>/delete/", views.service_delete, name="service_delete"),

    # Projects
    path("projects/", views.projects_list, name="projects"),
    path("projects/add/", views.project_add, name="project_add"),
    path("projects/<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),

    # Reviews / Testimonials
    path("reviews/", views.reviews_list, name="reviews"),
    path("reviews/add/", views.review_add, name="review_add"),
    path("reviews/<int:pk>/edit/", views.review_edit, name="review_edit"),
    path("reviews/<int:pk>/delete/", views.review_delete, name="review_delete"),
]
