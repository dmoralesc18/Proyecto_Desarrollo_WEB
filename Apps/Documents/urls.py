from django.urls import path
from .views import (
    DocumentsView,
    DocumentCreateView,
    DocumentDetailView,
    DocumentUpdateView,
    DocumentDeleteView
)

app_name = 'documents'

urlpatterns = [
    path('', DocumentsView.as_view(), name='documentsapp'),
    path('create/', DocumentCreateView.as_view(), name='document_create'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('<int:pk>/edit/', DocumentUpdateView.as_view(), name='document_update'),
    path('<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
]