from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Inspeccion, Incidente, Certificacion, PruebaCalidad
from .forms import InspeccionForm, IncidenteForm, CertificacionForm, PruebaCalidadForm

class QualityView(TemplateView):
    template_name = 'quality.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_inspecciones'] = Inspeccion.objects.count()
        context['total_incidentes'] = Incidente.objects.count()
        context['total_certificaciones'] = Certificacion.objects.count()
        context['total_pruebas'] = PruebaCalidad.objects.count()
        return context

# ==================== INSPECCIONES ====================
class InspeccionListView(ListView):
    model = Inspeccion
    template_name = 'inspeccion_list.html'
    context_object_name = 'inspecciones'
    ordering = ['-fecha']

class InspeccionDetailView(DetailView):
    model = Inspeccion
    template_name = 'inspeccion_detail.html'
    context_object_name = 'inspeccion'
    pk_url_kwarg = 'pk'

class InspeccionCreateView(CreateView):
    model = Inspeccion
    form_class = InspeccionForm
    template_name = 'inspeccion_form.html'
    success_url = reverse_lazy('quality:inspeccion_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Inspection'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Inspection created successfully.')
        return super().form_valid(form)

class InspeccionUpdateView(UpdateView):
    model = Inspeccion
    form_class = InspeccionForm
    template_name = 'inspeccion_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Inspection'
        return context
    
    def get_success_url(self):
        return reverse_lazy('quality:inspeccion_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Inspection updated successfully.')
        return super().form_valid(form)

class InspeccionDeleteView(DeleteView):
    model = Inspeccion
    template_name = 'inspeccion_delete.html'
    context_object_name = 'inspeccion'
    success_url = reverse_lazy('quality:inspeccion_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Inspection deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== INCIDENTES ====================
class IncidenteListView(ListView):
    model = Incidente
    template_name = 'incidente_list.html'
    context_object_name = 'incidentes'
    ordering = ['-fecha']

class IncidenteDetailView(DetailView):
    model = Incidente
    template_name = 'incidente_detail.html'
    context_object_name = 'incidente'
    pk_url_kwarg = 'pk'

class IncidenteCreateView(CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'incidente_form.html'
    success_url = reverse_lazy('quality:incidente_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Incident'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Incident created successfully.')
        return super().form_valid(form)

class IncidenteUpdateView(UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'incidente_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Incident'
        return context
    
    def get_success_url(self):
        return reverse_lazy('quality:incidente_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Incident updated successfully.')
        return super().form_valid(form)

class IncidenteDeleteView(DeleteView):
    model = Incidente
    template_name = 'incidente_delete.html'
    context_object_name = 'incidente'
    success_url = reverse_lazy('quality:incidente_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Incident deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== CERTIFICACIONES ====================
class CertificacionListView(ListView):
    model = Certificacion
    template_name = 'certificacion_list.html'
    context_object_name = 'certificaciones'
    ordering = ['-fecha_emision']

class CertificacionDetailView(DetailView):
    model = Certificacion
    template_name = 'certificacion_detail.html'
    context_object_name = 'certificacion'
    pk_url_kwarg = 'pk'

class CertificacionCreateView(CreateView):
    model = Certificacion
    form_class = CertificacionForm
    template_name = 'certificacion_form.html'
    success_url = reverse_lazy('quality:certificacion_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Certification'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification created successfully.')
        return super().form_valid(form)

class CertificacionUpdateView(UpdateView):
    model = Certificacion
    form_class = CertificacionForm
    template_name = 'certificacion_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Certification'
        return context
    
    def get_success_url(self):
        return reverse_lazy('quality:certificacion_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully.')
        return super().form_valid(form)

class CertificacionDeleteView(DeleteView):
    model = Certificacion
    template_name = 'certificacion_delete.html'
    context_object_name = 'certificacion'
    success_url = reverse_lazy('quality:certificacion_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Certification deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== PRUEBAS DE CALIDAD ====================
class PruebaCalidadListView(ListView):
    model = PruebaCalidad
    template_name = 'prueba_list.html'
    context_object_name = 'pruebas'
    ordering = ['-fecha']

class PruebaCalidadDetailView(DetailView):
    model = PruebaCalidad
    template_name = 'prueba_detail.html'
    context_object_name = 'prueba'
    pk_url_kwarg = 'pk'

class PruebaCalidadCreateView(CreateView):
    model = PruebaCalidad
    form_class = PruebaCalidadForm
    template_name = 'prueba_form.html'
    success_url = reverse_lazy('quality:prueba_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Quality Test'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Quality test created successfully.')
        return super().form_valid(form)

class PruebaCalidadUpdateView(UpdateView):
    model = PruebaCalidad
    form_class = PruebaCalidadForm
    template_name = 'prueba_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Quality Test'
        return context
    
    def get_success_url(self):
        return reverse_lazy('quality:prueba_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Quality test updated successfully.')
        return super().form_valid(form)

class PruebaCalidadDeleteView(DeleteView):
    model = PruebaCalidad
    template_name = 'prueba_delete.html'
    context_object_name = 'prueba'
    success_url = reverse_lazy('quality:prueba_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Quality test deleted successfully.')
        return super().delete(request, *args, **kwargs)