from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.utils import timezone

from .models import Post, Category


def blog_list(request):
    posts = Post.published.select_related("category", "author").prefetch_related("tags")
    featured = posts.filter(is_featured=True).first()
    if featured:
        regular = posts.exclude(pk=featured.pk)
    else:
        regular = posts

    paginator = Paginator(regular, 9)
    page = request.GET.get("page", 1)
    page_obj = paginator.get_page(page)

    return render(request, "blog/list.html", {
        "featured": featured,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("category", "author").prefetch_related("tags"),
        slug=slug,
        status="published",
        published_at__lte=timezone.now(),
    )

    Post.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)

    related = (
        Post.published.filter(category=post.category)
        .exclude(pk=post.pk)
        .select_related("category")[:3]
    )

    # Prev/next
    try:
        prev_post = Post.published.filter(published_at__lt=post.published_at).first()
    except Post.DoesNotExist:
        prev_post = None
    try:
        next_post = Post.published.filter(published_at__gt=post.published_at).last()
    except Post.DoesNotExist:
        next_post = None

    return render(request, "blog/detail.html", {
        "post": post,
        "related": related,
        "prev_post": prev_post,
        "next_post": next_post,
    })


def blog_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related("category", "author")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
    })


def blog_search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if q:
        results = (
            Post.published
            .filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(body__icontains=q))
            .select_related("category", "author")
            .distinct()
        )
    paginator = Paginator(results, 9)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/search_results.html", {
        "q": q,
        "page_obj": page_obj,
    })
