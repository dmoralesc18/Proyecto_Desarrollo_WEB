from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Fuerza a que toda la aplicación requiera sesión iniciada.
    Excepciones: página de login y archivos estáticos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir recursos estáticos
        static_url = getattr(settings, 'STATIC_URL', '/static/') or '/static/'
        path = request.path or '/'
        if path.startswith(static_url):
            return self.get_response(request)

        # Permitir panel de administración de Django
        if path.startswith('/admin/'):
            return self.get_response(request)

        # Permitir login y logout endpoints explícitos
        login_path = reverse('core:login')
        logout_path = reverse('core:logout')

        allowed_paths = {login_path, logout_path}
        if path in allowed_paths:
            return self.get_response(request)

        # Si no hay usuario autenticado de Django, redirigir a login
        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            return redirect('core:login')

        return self.get_response(request)
