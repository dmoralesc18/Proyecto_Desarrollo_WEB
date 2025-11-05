from django.contrib import messages
from django.shortcuts import redirect


class AdminOnlyMixin:
    """Allow only Django superusers. Redirects to home with message otherwise."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if not request.user.is_superuser:
            messages.error(request, 'No tiene permisos para acceder a esta página.')
            return redirect('homeapp')
        return super().dispatch(request, *args, **kwargs)


class StaffReadOnlyMixin:
    """For staff (supervisor) allow only safe methods; admin full access; others blocked for unsafe."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        # staff but not superuser: block write methods
        if request.user.is_staff and request.method not in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return super().dispatch(request, *args, **kwargs)
        if request.user.is_staff:
            messages.error(request, 'Perfil supervisor solo lectura: acción no permitida.')
            return redirect('homeapp')
        # clients/others
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permisos para esta acción.')
        return redirect('homeapp')


class AdminOrStaffMixin:
    """Allow superusers and staff; block others."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permisos para acceder a esta página.')
        return redirect('homeapp')
