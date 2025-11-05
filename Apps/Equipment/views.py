from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.utils import OperationalError, ProgrammingError
from Apps.Core.permissions import AdminOnlyMixin, AdminOrStaffMixin
from Apps.Equipment.models import MaquinariaEquipo, Alquiler
from .forms import MaquinariaEquipoForm, AlquilerForm

# ============================================
# VISTAS DE MAQUINARIA/EQUIPO
# ============================================

class EquipmentView(AdminOrStaffMixin, ListView):
    model = MaquinariaEquipo
    template_name = 'equipment.html'
    context_object_name = 'equipos'
    
    def get_queryset(self):
        qs = MaquinariaEquipo.objects.all()
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Tablas de equipos no existen en la BD local.')
            return MaquinariaEquipo.objects.none()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['alquileres'] = Alquiler.objects.all()
        except (OperationalError, ProgrammingError):
            context['alquileres'] = Alquiler.objects.none()
        return context

class EquipmentDetailView(AdminOrStaffMixin, DetailView):
    model = MaquinariaEquipo
    template_name = 'equipment_detail.html'
    context_object_name = 'equipo'
    pk_url_kwarg = 'pk'

class EquipmentCreateView(AdminOrStaffMixin, CreateView):
    model = MaquinariaEquipo
    form_class = MaquinariaEquipoForm
    template_name = 'equipment_form.html'
    success_url = reverse_lazy('equipmentapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Equipment'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipment created successfully.')
        return super().form_valid(form)

class EquipmentUpdateView(AdminOnlyMixin, UpdateView):
    model = MaquinariaEquipo
    form_class = MaquinariaEquipoForm
    template_name = 'equipment_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Equipment'
        return context
    
    def get_success_url(self):
        return reverse_lazy('equipment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipment updated successfully.')
        return super().form_valid(form)

class EquipmentDeleteView(AdminOnlyMixin, DeleteView):
    model = MaquinariaEquipo
    template_name = 'equipment_delete.html'
    context_object_name = 'equipo'
    success_url = reverse_lazy('equipmentapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Equipment deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE ALQUILER
# ============================================

class RentalDetailView(DetailView):
    model = Alquiler
    template_name = 'rental_detail.html'
    context_object_name = 'alquiler'
    pk_url_kwarg = 'pk'

class RentalCreateView(AdminOrStaffMixin, CreateView):
    model = Alquiler
    form_class = AlquilerForm
    template_name = 'rental_form.html'
    success_url = reverse_lazy('equipmentapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Rental'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Rental created successfully.')
        return super().form_valid(form)

class RentalUpdateView(AdminOnlyMixin, UpdateView):
    model = Alquiler
    form_class = AlquilerForm
    template_name = 'rental_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Rental'
        return context
    
    def get_success_url(self):
        return reverse_lazy('rental_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Rental updated successfully.')
        return super().form_valid(form)

class RentalDeleteView(AdminOnlyMixin, DeleteView):
    model = Alquiler
    template_name = 'rental_delete.html'
    context_object_name = 'alquiler'
    success_url = reverse_lazy('equipmentapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Rental deleted successfully.')
        return super().delete(request, *args, **kwargs)
