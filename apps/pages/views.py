from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Service, Project, Testimonial, Stat, ContactMessage
from .forms import ContactForm
from apps.blog.models import Post


def home(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactMessage.objects.create(
                name=cd["name"],
                email=cd["email"],
                subject=cd["subject"],
                message=cd["message"],
            )
            messages.success(request, "Thanks! We'll be in touch soon.")
            return redirect("pages:home")

    ctx = {
        "services": Service.objects.filter(is_active=True)[:6],
        "projects": Project.objects.all()[:4],
        "testimonials": Testimonial.objects.filter(is_active=True),
        "stats": Stat.objects.all(),
        "latest_posts": Post.published.select_related("category", "author")[:4],
        "form": form,
    }
    return render(request, "pages/index.html", ctx)


def about(request):
    return render(request, "pages/about.html", {
        "stats": Stat.objects.all(),
        "testimonials": Testimonial.objects.filter(is_active=True),
    })


def services(request):
    return render(request, "pages/service.html", {
        "services": Service.objects.filter(is_active=True),
    })


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactMessage.objects.create(
                name=cd["name"],
                email=cd["email"],
                subject=cd["subject"],
                message=cd["message"],
            )
            messages.success(request, "Message sent! We'll get back to you within 24 hours.")
            return redirect("pages:contact")
    return render(request, "pages/contact.html", {"form": form})


def privacy(request):
    return render(request, "pages/privacy.html")


def faq(request):
    return render(request, "pages/faq.html")


def career(request):
    return render(request, "pages/career.html")


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related = Service.objects.filter(is_active=True).exclude(slug=slug)[:4]
    return render(request, "pages/service_detail.html", {
        "service": service,
        "related": related,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(filter_group=project.filter_group).exclude(slug=slug)[:3]
    return render(request, "pages/project_detail.html", {
        "project": project,
        "related": related,
    })


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
