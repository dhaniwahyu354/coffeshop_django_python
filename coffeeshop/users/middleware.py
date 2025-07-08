from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [
     '/',  # ← tambahkan ini!
    '/auth/login/',
    '/auth/register/',
    '/auth/logout/',
    '/privacy-policy/',
    '/admin/',
    '/static/',      # untuk file statis
    '/media/',       # jika kamu pakai media
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print(f"[Middleware] Mendeteksi path: {path}")
        print(f"[Middleware] User login? {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                print("[Middleware] User belum login. Redirect ke login page.")
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)
