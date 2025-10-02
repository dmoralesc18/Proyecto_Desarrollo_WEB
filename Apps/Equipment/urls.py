from django.urls import path
from .views import (
    EquipmentView,
    EquipmentCreateView,
    EquipmentDetailView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    RentalCreateView,
    RentalDetailView,
    RentalUpdateView,
    RentalDeleteView
)

urlpatterns = [
    # Equipment URLs
    path('', EquipmentView.as_view(), name='equipmentapp'),
    path('create/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('<int:pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Rentals URLs
    path('rental/create/', RentalCreateView.as_view(), name='rental_create'),
    path('rental/<int:pk>/', RentalDetailView.as_view(), name='rental_detail'),
    path('rental/<int:pk>/edit/', RentalUpdateView.as_view(), name='rental_update'),
    path('rental/<int:pk>/delete/', RentalDeleteView.as_view(), name='rental_delete'),
]