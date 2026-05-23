from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from apps.pages.models import Service, Project, Testimonial, ContactMessage, SiteVisit
from .forms import DashboardLoginForm, ServiceForm, ProjectForm, ReviewForm


def dashboard_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect("dashboard:login")
    return wrapper


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard:home")
    form = DashboardLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get("next", "dashboard:home"))
    return render(request, "dashboard/login.html", {"form": form})


def dashboard_logout(request):
    logout(request)
    return redirect("dashboard:login")


@dashboard_required
def dashboard_home(request):
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_services = Service.objects.count()
    total_projects = Project.objects.count()
    total_reviews = Testimonial.objects.count()
    latest_messages = ContactMessage.objects.filter(is_read=False)[:5]

    # Last 7 days visits
    today = timezone.localdate()
    last_7 = []
    max_count = 1
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        try:
            visit = SiteVisit.objects.get(date=day)
            count = visit.count
        except SiteVisit.DoesNotExist:
            count = 0
        last_7.append({"date": day.strftime("%a"), "count": count})
        if count > max_count:
            max_count = count

    # Add percentage for bar height
    for item in last_7:
        item["pct"] = round((item["count"] / max_count) * 100) if max_count else 0

    ctx = {
        "total_messages": total_messages,
        "unread_messages": unread_messages,
        "total_services": total_services,
        "total_projects": total_projects,
        "total_reviews": total_reviews,
        "latest_messages": latest_messages,
        "last_7": last_7,
    }
    return render(request, "dashboard/index.html", ctx)


# ── Messages ─────────────────────────────────────────────────────────────────

@dashboard_required
def messages_list(request):
    msgs = ContactMessage.objects.all()
    return render(request, "dashboard/messages.html", {"msgs": msgs})


@dashboard_required
def message_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save(update_fields=["is_read"])
    return redirect("dashboard:messages")


@dashboard_required
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        msg.delete()
        messages.success(request, "Message deleted.")
    return redirect("dashboard:messages")


# ── Services ──────────────────────────────────────────────────────────────────

@dashboard_required
def services_list(request):
    svcs = Service.objects.all()
    return render(request, "dashboard/services.html", {"svcs": svcs})


@dashboard_required
def service_add(request):
    form = ServiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Service added.")
        return redirect("dashboard:services")
    return render(request, "dashboard/service_form.html", {"form": form, "action": "Add Service"})


@dashboard_required
def service_edit(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, instance=svc)
    if form.is_valid():
        form.save()
        messages.success(request, "Service updated.")
        return redirect("dashboard:services")
    return render(request, "dashboard/service_form.html", {"form": form, "action": "Edit Service", "obj": svc})


@dashboard_required
def service_delete(request, pk):
    svc = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        svc.delete()
        messages.success(request, "Service deleted.")
    return redirect("dashboard:services")


# ── Projects ──────────────────────────────────────────────────────────────────

@dashboard_required
def projects_list(request):
    projects = Project.objects.all()
    return render(request, "dashboard/projects.html", {"projects": projects})


@dashboard_required
def project_add(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Project added.")
        return redirect("dashboard:projects")
    return render(request, "dashboard/project_form.html", {"form": form, "action": "Add Project"})


@dashboard_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, "Project updated.")
        return redirect("dashboard:projects")
    return render(request, "dashboard/project_form.html", {"form": form, "action": "Edit Project", "obj": project})


@dashboard_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted.")
    return redirect("dashboard:projects")


# ── Reviews ───────────────────────────────────────────────────────────────────

@dashboard_required
def reviews_list(request):
    reviews = Testimonial.objects.all()
    return render(request, "dashboard/reviews.html", {"reviews": reviews})


@dashboard_required
def review_add(request):
    form = ReviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Review added.")
        return redirect("dashboard:reviews")
    return render(request, "dashboard/review_form.html", {"form": form, "action": "Add Review"})


@dashboard_required
def review_edit(request, pk):
    review = get_object_or_404(Testimonial, pk=pk)
    form = ReviewForm(request.POST or None, request.FILES or None, instance=review)
    if form.is_valid():
        form.save()
        messages.success(request, "Review updated.")
        return redirect("dashboard:reviews")
    return render(request, "dashboard/review_form.html", {"form": form, "action": "Edit Review", "obj": review})


@dashboard_required
def review_delete(request, pk):
    review = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted.")
    return redirect("dashboard:reviews")
