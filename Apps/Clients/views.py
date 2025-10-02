from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Apps.Clients.models import Cliente
from .forms import ClienteForm

class ClientsView(ListView):
    model = Cliente
    template_name = 'clients.html'
    context_object_name = 'clientes'
    
class ClientDetailView(DetailView):
    model = Cliente
    template_name = 'client_detail.html'
    context_object_name = 'cliente'
    pk_url_kwarg = 'pk'

class ClientCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('clients:clientsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Client'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Client created successfully.')
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'client_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Client'
        return context
    
    def get_success_url(self):
        return reverse_lazy('clients:client_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Client updated successfully.')
        return super().form_valid(form)

class ClientDeleteView(DeleteView):
    model = Cliente
    template_name = 'client_delete.html'
    context_object_name = 'cliente'
    success_url = reverse_lazy('clients:clients')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Client deleted successfully.')
        return super().delete(request, *args, **kwargs)