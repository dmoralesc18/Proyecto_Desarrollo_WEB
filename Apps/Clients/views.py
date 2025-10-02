from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class ClientsView(TemplateView):
    template_name = 'clients.html'