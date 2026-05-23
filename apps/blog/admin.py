from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "is_featured", "view_count", "published_at", "thumb_preview")
    list_filter = ("status", "category", "is_featured", "tags")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    readonly_fields = ("view_count", "reading_time", "published_at", "created_at", "updated_at", "thumb_preview")
    actions = ["publish_posts", "unpublish_posts"]

    fieldsets = (
        ("Content", {
            "fields": ("title", "slug", "excerpt", "body", "category", "tags", "author"),
        }),
        ("Media", {
            "fields": ("thumbnail", "thumb_preview", "youtube_url"),
            "description": "Provide an image OR a YouTube URL. If both given, image takes priority for thumbnail.",
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "og_image"),
            "classes": ("collapse",),
        }),
        ("Publishing", {
            "fields": ("status", "is_featured", "view_count", "reading_time", "published_at", "created_at", "updated_at"),
        }),
    )

    def thumb_preview(self, obj):
        url = obj.thumb_url
        if url:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', url)
        return "—"
    thumb_preview.short_description = "Preview"

    def publish_posts(self, request, queryset):
        queryset.update(status="published", published_at=timezone.now())
    publish_posts.short_description = "Publish selected posts"

    def unpublish_posts(self, request, queryset):
        queryset.update(status="draft")
    unpublish_posts.short_description = "Unpublish selected posts"
