from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class EquipmentView(TemplateView):
    template_name = 'equipment.html'
