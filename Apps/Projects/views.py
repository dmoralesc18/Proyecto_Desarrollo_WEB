from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Apps.Core.permissions import AdminOnlyMixin, AdminOrStaffMixin
from Apps.Projects.models import Proyecto, Presupuesto
from .forms import ProyectoForm, PresupuestoForm

class ProjectsView(ListView):
    model = Proyecto
    template_name = 'projects.html'
    context_object_name = 'proyectos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            if user.is_superuser or user.is_staff:
                context['presupuestos'] = Presupuesto.objects.all()
        except Exception:
            context['presupuestos'] = Presupuesto.objects.none()
        return context
    
class ProjectDetailView(DetailView):
    model = Proyecto
    template_name = 'project_detail.html'
    context_object_name = 'proyecto'
    pk_url_kwarg = 'pk'

class ProjectCreateView(AdminOrStaffMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'project_form.html'
    success_url = reverse_lazy('projectsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Project'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully.')
        return super().form_valid(form)

class ProjectUpdateView(AdminOnlyMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'project_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Project'
        return context
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully.')
        return super().form_valid(form)

class ProjectDeleteView(AdminOnlyMixin, DeleteView):
    model = Proyecto
    template_name = 'project_delete.html'
    context_object_name = 'proyecto'
    success_url = reverse_lazy('projectsapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE PRESUPUESTO
# ============================================

class BudgetDetailView(DetailView):
    model = Presupuesto
    template_name = 'budget_detail.html'
    context_object_name = 'presupuesto'
    pk_url_kwarg = 'pk'

class BudgetCreateView(AdminOrStaffMixin, CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'budget_form.html'
    success_url = reverse_lazy('projectsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Budget'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Budget created successfully.')
        return super().form_valid(form)

class BudgetUpdateView(AdminOnlyMixin, UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'budget_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Budget'
        return context
    
    def get_success_url(self):
        return reverse_lazy('budget_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully.')
        return super().form_valid(form)

class BudgetDeleteView(AdminOnlyMixin, DeleteView):
    model = Presupuesto
    template_name = 'budget_delete.html'
    context_object_name = 'presupuesto'
    success_url = reverse_lazy('projectsapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Budget deleted successfully.')
        return super().delete(request, *args, **kwargs)
