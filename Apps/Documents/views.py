from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import DocumentoTecnico
from .forms import DocumentoTecnicoForm

class DocumentsView(ListView):
    model = DocumentoTecnico
    template_name = 'documents.html'
    context_object_name = 'documentos'
    ordering = ['-fecha_carga']

class DocumentDetailView(DetailView):
    model = DocumentoTecnico
    template_name = 'document_detail.html'
    context_object_name = 'documento'
    pk_url_kwarg = 'pk'

class DocumentCreateView(CreateView):
    model = DocumentoTecnico
    form_class = DocumentoTecnicoForm
    template_name = 'document_form.html'
    success_url = reverse_lazy('documents:documentsapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Document'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Document created successfully.')
        return super().form_valid(form)

class DocumentUpdateView(UpdateView):
    model = DocumentoTecnico
    form_class = DocumentoTecnicoForm
    template_name = 'document_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Document'
        return context
    
    def get_success_url(self):
        return reverse_lazy('documents:document_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Document updated successfully.')
        return super().form_valid(form)

class DocumentDeleteView(DeleteView):
    model = DocumentoTecnico
    template_name = 'document_delete.html'
    context_object_name = 'documento'
    success_url = reverse_lazy('documents:documentsapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Document deleted successfully.')
        return super().delete(request, *args, **kwargs)