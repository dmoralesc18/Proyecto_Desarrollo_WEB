from django.contrib import admin
from django.urls import path, include
from Apps.Equipment import views
from .views import EquipmentView

urlpatterns = [
   path('', EquipmentView.as_view(), name='equipmentapp'),
]