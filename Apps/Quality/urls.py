from django.urls import path
from .views import (
    QualityView,
    # Inspecciones
    InspeccionListView,
    InspeccionCreateView,
    InspeccionDetailView,
    InspeccionUpdateView,
    InspeccionDeleteView,
    # Incidentes
    IncidenteListView,
    IncidenteCreateView,
    IncidenteDetailView,
    IncidenteUpdateView,
    IncidenteDeleteView,
    # Certificaciones
    CertificacionListView,
    CertificacionCreateView,
    CertificacionDetailView,
    CertificacionUpdateView,
    CertificacionDeleteView,
    # Pruebas de Calidad
    PruebaCalidadListView,
    PruebaCalidadCreateView,
    PruebaCalidadDetailView,
    PruebaCalidadUpdateView,
    PruebaCalidadDeleteView,
)

app_name = 'quality'

urlpatterns = [
    path('', QualityView.as_view(), name='qualityapp'),
    
    # Inspecciones
    path('inspections/', InspeccionListView.as_view(), name='inspeccion_list'),
    path('inspections/create/', InspeccionCreateView.as_view(), name='inspeccion_create'),
    path('inspections/<int:pk>/', InspeccionDetailView.as_view(), name='inspeccion_detail'),
    path('inspections/<int:pk>/edit/', InspeccionUpdateView.as_view(), name='inspeccion_update'),
    path('inspections/<int:pk>/delete/', InspeccionDeleteView.as_view(), name='inspeccion_delete'),
    
    # Incidentes
    path('incidents/', IncidenteListView.as_view(), name='incidente_list'),
    path('incidents/create/', IncidenteCreateView.as_view(), name='incidente_create'),
    path('incidents/<int:pk>/', IncidenteDetailView.as_view(), name='incidente_detail'),
    path('incidents/<int:pk>/edit/', IncidenteUpdateView.as_view(), name='incidente_update'),
    path('incidents/<int:pk>/delete/', IncidenteDeleteView.as_view(), name='incidente_delete'),
    
    # Certificaciones
    path('certifications/', CertificacionListView.as_view(), name='certificacion_list'),
    path('certifications/create/', CertificacionCreateView.as_view(), name='certificacion_create'),
    path('certifications/<int:pk>/', CertificacionDetailView.as_view(), name='certificacion_detail'),
    path('certifications/<int:pk>/edit/', CertificacionUpdateView.as_view(), name='certificacion_update'),
    path('certifications/<int:pk>/delete/', CertificacionDeleteView.as_view(), name='certificacion_delete'),
    
    # Pruebas de Calidad
    path('tests/', PruebaCalidadListView.as_view(), name='prueba_list'),
    path('tests/create/', PruebaCalidadCreateView.as_view(), name='prueba_create'),
    path('tests/<int:pk>/', PruebaCalidadDetailView.as_view(), name='prueba_detail'),
    path('tests/<int:pk>/edit/', PruebaCalidadUpdateView.as_view(), name='prueba_update'),
    path('tests/<int:pk>/delete/', PruebaCalidadDeleteView.as_view(), name='prueba_delete'),
]