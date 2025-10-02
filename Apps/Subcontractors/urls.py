from django.urls import path
from .views import (
    SubcontractorsView,
    SubcontractorCreateView,
    SubcontractorDetailView,
    SubcontractorUpdateView,
    SubcontractorDeleteView,
    ContractCreateView,
    ContractDetailView,
    ContractUpdateView,
    ContractDeleteView
)

urlpatterns = [
    # Subcontractors URLs
    path('', SubcontractorsView.as_view(), name='subcontractorsapp'),
    path('create/', SubcontractorCreateView.as_view(), name='subcontractor_create'),
    path('<int:pk>/', SubcontractorDetailView.as_view(), name='subcontractor_detail'),
    path('<int:pk>/edit/', SubcontractorUpdateView.as_view(), name='subcontractor_update'),
    path('<int:pk>/delete/', SubcontractorDeleteView.as_view(), name='subcontractor_delete'),
    
    # Contracts URLs
    path('contract/create/', ContractCreateView.as_view(), name='contract_create'),
    path('contract/<int:pk>/', ContractDetailView.as_view(), name='contract_detail'),
    path('contract/<int:pk>/edit/', ContractUpdateView.as_view(), name='contract_update'),
    path('contract/<int:pk>/delete/', ContractDeleteView.as_view(), name='contract_delete'),
]