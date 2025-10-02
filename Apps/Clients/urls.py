from django.contrib import admin
from django.urls import path, include
from Apps.Clients import views
from .views import ClientsView

urlpatterns = [
   path('clients/', ClientsView.as_view(), name='clientsapp'),
]