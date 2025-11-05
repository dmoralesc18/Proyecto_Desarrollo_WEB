from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model


class LoginRequiredMiddleware:
    """
    Fuerza a que toda la aplicación requiera sesión iniciada.
    Excepciones: login, logout, setup inicial y archivos estáticos.
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

        # Permitir login/logout y setup de primer usuario
        login_path = reverse('core:login')
        logout_path = reverse('core:logout')
        setup_path = reverse('core:first_user_setup')
        allowed_paths = {login_path, logout_path, setup_path}

        # Si no existe superusuario, forzar a la página de setup
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists() and path not in allowed_paths:
            return redirect('core:first_user_setup')

        if path in allowed_paths:
            return self.get_response(request)

        # Si no hay usuario autenticado de Django, redirigir a login
        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            return redirect('core:login')

        return self.get_response(request)

