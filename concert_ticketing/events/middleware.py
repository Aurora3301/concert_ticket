from django.http import HttpResponseForbidden
from django.core.cache import cache

class DDOSProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"request_count_{ip}"
        count = cache.get(key, 0)
        
        if count > 100:  # Adjust threshold as needed
            return HttpResponseForbidden("Too many requests")
        
        cache.set(key, count + 1, 60)  # 1 minute window
        return self.get_response(request)