from django.contrib import admin
from django.urls import path
from Apps.Clients import views
from django.urls import path
from .views import (
    ClientsView,
    ClientCreateView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView
)

app_name = 'clients'

urlpatterns = [
    path('', ClientsView.as_view(), name='clientsapp'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]