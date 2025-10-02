from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class SubcontractorsView(TemplateView):
    template_name = 'subcontractors.html'