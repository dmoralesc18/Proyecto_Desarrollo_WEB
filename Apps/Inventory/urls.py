from django.contrib import admin
from django.urls import path, include
from Apps.Inventory import views
from .views import InventoryView

urlpatterns = [
   path('', InventoryView.as_view(), name='inventoryapp'),
]