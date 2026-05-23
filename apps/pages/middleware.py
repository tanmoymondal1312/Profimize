from django.db.models import F
from django.utils import timezone


_SKIP_PREFIXES = ("/static/", "/media/", "/dashboard/", "/admin/", "/ckeditor5/", "/favicon")


class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == "GET" and response.status_code == 200:
            path = request.path
            if not any(path.startswith(p) for p in _SKIP_PREFIXES):
                try:
                    from .models import SiteVisit
                    today = timezone.localdate()
                    obj, created = SiteVisit.objects.get_or_create(date=today, defaults={"count": 1})
                    if not created:
                        SiteVisit.objects.filter(date=today).update(count=F("count") + 1)
                except Exception:
                    pass
        return response
