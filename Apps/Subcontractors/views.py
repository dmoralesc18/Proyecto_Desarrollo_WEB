from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Apps.Subcontractors.models import Subcontratista, Contrato
from .forms import SubcontratistaForm, ContratoForm

# ============================================
# VISTAS DE SUBCONTRATISTA
# ============================================

class SubcontractorsView(ListView):
    model = Subcontratista
    template_name = 'subcontractors.html'
    context_object_name = 'subcontratistas'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contratos'] = Contrato.objects.all()
        return context

class SubcontractorDetailView(DetailView):
    model = Subcontratista
    template_name = 'subcontractor_detail.html'
    context_object_name = 'subcontratista'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener contratos del subcontratista
        context['contratos'] = Contrato.objects.filter(id_subcontratista=self.object)
        return context

class SubcontractorCreateView(CreateView):
    model = Subcontratista
    form_class = SubcontratistaForm
    template_name = 'subcontractor_form.html'
    success_url = reverse_lazy('subcontractorsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Subcontractor'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcontractor created successfully.')
        return super().form_valid(form)

class SubcontractorUpdateView(UpdateView):
    model = Subcontratista
    form_class = SubcontratistaForm
    template_name = 'subcontractor_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Subcontractor'
        return context
    
    def get_success_url(self):
        return reverse_lazy('subcontractor_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Subcontractor updated successfully.')
        return super().form_valid(form)

class SubcontractorDeleteView(DeleteView):
    model = Subcontratista
    template_name = 'subcontractor_delete.html'
    context_object_name = 'subcontratista'
    success_url = reverse_lazy('subcontractorsapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Subcontractor deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE CONTRATO
# ============================================

class ContractDetailView(DetailView):
    model = Contrato
    template_name = 'contract_detail.html'
    context_object_name = 'contrato'
    pk_url_kwarg = 'pk'

class ContractCreateView(CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contract_form.html'
    success_url = reverse_lazy('subcontractorsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Contract'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Contract created successfully.')
        return super().form_valid(form)

class ContractUpdateView(UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contract_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Contract'
        return context
    
    def get_success_url(self):
        return reverse_lazy('contract_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Contract updated successfully.')
        return super().form_valid(form)

class ContractDeleteView(DeleteView):
    model = Contrato
    template_name = 'contract_delete.html'
    context_object_name = 'contrato'
    success_url = reverse_lazy('subcontractorsapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contract deleted successfully.')
        return super().delete(request, *args, **kwargs)