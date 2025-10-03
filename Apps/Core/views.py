from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import SoporteForm

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