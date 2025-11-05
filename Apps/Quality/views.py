from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.utils import OperationalError, ProgrammingError
from Apps.Core.permissions import AdminOnlyMixin, AdminOrStaffMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Inspeccion, Incidente, Certificacion, PruebaCalidad
from .forms import InspeccionForm, IncidenteForm, CertificacionForm, PruebaCalidadForm

class QualityView(TemplateView):
    template_name = 'quality.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['total_inspecciones'] = Inspeccion.objects.count()
            context['total_incidentes'] = Incidente.objects.count()
            context['total_certificaciones'] = Certificacion.objects.count()
            context['total_pruebas'] = PruebaCalidad.objects.count()
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Faltan tablas de Calidad. Ejecuta migrate y sync_sqlite.')
            context['total_inspecciones'] = 0
            context['total_incidentes'] = 0
            context['total_certificaciones'] = 0
            context['total_pruebas'] = 0
        return context

# ==================== INSPECCIONES ====================
class InspeccionListView(AdminOrStaffMixin, ListView):
    model = Inspeccion
    template_name = 'inspeccion_list.html'
    context_object_name = 'inspecciones'
    ordering = ['-fecha']
    def get_queryset(self):
        qs = Inspeccion.objects.all().order_by('-fecha')
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Tabla de inspecciones inexistente en la BD local.')
            return Inspeccion.objects.none()
        return qs

class InspeccionDetailView(AdminOrStaffMixin, DetailView):
    model = Inspeccion
    template_name = 'inspeccion_detail.html'
    context_object_name = 'inspeccion'
    pk_url_kwarg = 'pk'

class InspeccionCreateView(AdminOrStaffMixin, CreateView):
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

class InspeccionUpdateView(AdminOnlyMixin, UpdateView):
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

class InspeccionDeleteView(AdminOnlyMixin, DeleteView):
    model = Inspeccion
    template_name = 'inspeccion_delete.html'
    context_object_name = 'inspeccion'
    success_url = reverse_lazy('quality:inspeccion_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Inspection deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== INCIDENTES ====================
class IncidenteListView(AdminOrStaffMixin, ListView):
    model = Incidente
    template_name = 'incidente_list.html'
    context_object_name = 'incidentes'
    ordering = ['-fecha']
    def get_queryset(self):
        qs = Incidente.objects.all().order_by('-fecha')
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Tabla de incidentes inexistente en la BD local.')
            return Incidente.objects.none()
        return qs

class IncidenteDetailView(AdminOrStaffMixin, DetailView):
    model = Incidente
    template_name = 'incidente_detail.html'
    context_object_name = 'incidente'
    pk_url_kwarg = 'pk'

class IncidenteCreateView(AdminOrStaffMixin, CreateView):
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

class IncidenteUpdateView(AdminOnlyMixin, UpdateView):
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

class IncidenteDeleteView(AdminOnlyMixin, DeleteView):
    model = Incidente
    template_name = 'incidente_delete.html'
    context_object_name = 'incidente'
    success_url = reverse_lazy('quality:incidente_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Incident deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== CERTIFICACIONES ====================
class CertificacionListView(AdminOrStaffMixin, ListView):
    model = Certificacion
    template_name = 'certificacion_list.html'
    context_object_name = 'certificaciones'
    ordering = ['-fecha_emision']
    def get_queryset(self):
        qs = Certificacion.objects.all().order_by('-fecha_emision')
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Tabla de certificaciones inexistente en la BD local.')
            return Certificacion.objects.none()
        return qs

class CertificacionDetailView(AdminOrStaffMixin, DetailView):
    model = Certificacion
    template_name = 'certificacion_detail.html'
    context_object_name = 'certificacion'
    pk_url_kwarg = 'pk'

class CertificacionCreateView(AdminOrStaffMixin, CreateView):
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

class CertificacionUpdateView(AdminOnlyMixin, UpdateView):
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

class CertificacionDeleteView(AdminOnlyMixin, DeleteView):
    model = Certificacion
    template_name = 'certificacion_delete.html'
    context_object_name = 'certificacion'
    success_url = reverse_lazy('quality:certificacion_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Certification deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== PRUEBAS DE CALIDAD ====================
class PruebaCalidadListView(AdminOrStaffMixin, ListView):
    model = PruebaCalidad
    template_name = 'prueba_list.html'
    context_object_name = 'pruebas'
    ordering = ['-fecha']
    def get_queryset(self):
        qs = PruebaCalidad.objects.all().order_by('-fecha')
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Tabla de pruebas de calidad inexistente en la BD local.')
            return PruebaCalidad.objects.none()
        return qs

class PruebaCalidadDetailView(AdminOrStaffMixin, DetailView):
    model = PruebaCalidad
    template_name = 'prueba_detail.html'
    context_object_name = 'prueba'
    pk_url_kwarg = 'pk'

class PruebaCalidadCreateView(AdminOrStaffMixin, CreateView):
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

class PruebaCalidadUpdateView(AdminOnlyMixin, UpdateView):
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

class PruebaCalidadDeleteView(AdminOnlyMixin, DeleteView):
    model = PruebaCalidad
    template_name = 'prueba_delete.html'
    context_object_name = 'prueba'
    success_url = reverse_lazy('quality:prueba_list')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Quality test deleted successfully.')
        return super().delete(request, *args, **kwargs)
