from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class DocumentsView(TemplateView):
    template_name = 'documents.html'