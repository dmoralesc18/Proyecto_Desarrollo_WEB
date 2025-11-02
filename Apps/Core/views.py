from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import SoporteForm, LoginForm, ProfileForm, UserForm
from .models import Usuario

# --- Simple auth helpers (session-based) ---
def require_login(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        return view_func(request, *args, **kwargs)
    return _wrapped

def require_admin(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
        if not request.user.is_superuser:
            messages.error(request, 'No tiene permisos para acceder a esta página.')
            return redirect('homeapp')
        return view_func(request, *args, **kwargs)
    return _wrapped

class SupportCreateView(FormView):
    form_class = SoporteForm
    template_name = 'support_form.html'
    success_url = reverse_lazy('core:support_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Technical Support'
        return context
    
    def form_valid(self, form):
        nombre = form.cleaned_data['nombre']
        correo = form.cleaned_data['correo']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        
        email_message = f"""
        New Support Request
        
        From: {nombre}
        Email: {correo}
        Subject: {asunto}
        
        Message:
        {mensaje}
        """
        
        try:
            send_mail(
                subject=f'Support Request: {asunto}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['support@yourcompany.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
        
        messages.success(self.request, 'Your support request has been submitted successfully.')
        return super().form_valid(form)


class SupportSuccessView(TemplateView):
    template_name = 'support_success.html'


# --- Auth views ---
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            # Autenticación por email -> obtener username y usar authenticate
            try:
                u = User.objects.get(email=correo)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                user = authenticate(request, username=correo, password=password)  # fallback si usan username en correo
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}')
                return redirect('homeapp')
            messages.error(request, 'Credenciales inválidas.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('core:login')


@require_login
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['nombre']
            user.email = form.cleaned_data['correo']
            pwd = form.cleaned_data['password']
            if pwd:
                user.set_password(pwd)
            user.save()
            # Si cambió password, mantener sesión
            if pwd:
                auth_login(request, user)
            messages.success(request, 'Perfil actualizado.')
            return redirect('core:profile')
    else:
        initial = {
            'nombre': user.first_name,
            'correo': user.email,
        }
        form = ProfileForm(initial=initial)
    return render(request, 'profile.html', {'form': form})


# --- User management (admin) ---
@require_admin
def user_list_view(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'usuarios': usuarios})


@require_admin
def user_create_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['correo']
            nombre = form.cleaned_data['nombre']
            rol = form.cleaned_data['rol']
            pwd = form.cleaned_data['password'] or User.objects.make_random_password()
            username = email  # simplificación: usar email como username
            u = User.objects.create_user(username=username, email=email, password=pwd)
            u.first_name = nombre
            # Mapear rol
            if rol == 'Administrador':
                u.is_staff = True
                u.is_superuser = True
            elif rol == 'Supervisor':
                u.is_staff = True
                u.is_superuser = False
            else:
                u.is_staff = False
                u.is_superuser = False
            u.save()
            messages.success(request, 'Usuario creado.')
            return redirect('core:users')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form, 'mode': 'create'})


@require_admin
def user_edit_view(request, pk: int):
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u.first_name = form.cleaned_data['nombre']
            u.email = form.cleaned_data['correo']
            rol = form.cleaned_data['rol']
            if rol == 'Administrador':
                u.is_staff = True
                u.is_superuser = True
            elif rol == 'Supervisor':
                u.is_staff = True
                u.is_superuser = False
            else:
                u.is_staff = False
                u.is_superuser = False
            pwd = form.cleaned_data['password']
            if pwd:
                u.set_password(pwd)
            u.save()
            messages.success(request, 'Usuario actualizado.')
            return redirect('core:users')
    else:
        initial = {
            'nombre': u.first_name,
            'correo': u.email,
            'rol': 'Administrador' if u.is_superuser else ('Supervisor' if u.is_staff else 'Cliente'),
        }
        form = UserForm(initial=initial)
    return render(request, 'user_form.html', {'form': form, 'mode': 'edit', 'usuario': u})


@require_admin
def user_delete_view(request, pk: int):
    u = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('core:users')
    return render(request, 'user_delete.html', {'usuario': u})
