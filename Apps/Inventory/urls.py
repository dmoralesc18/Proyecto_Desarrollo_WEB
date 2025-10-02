from django.urls import path
from .views import (
    InventoryView,
    MaterialCreateView,
    MaterialDetailView,
    MaterialUpdateView,
    MaterialDeleteView,
    InventarioCreateView,
    InventarioDetailView,
    InventarioUpdateView,
    InventarioDeleteView,
    InventarioMaterialCreateView,
    ProveedorCreateView,
    ProveedorDetailView,
    ProveedorUpdateView,
    ProveedorDeleteView,
    ProveedorMaterialCreateView,
)

urlpatterns = [
    # Main Inventory Page
    path('', InventoryView.as_view(), name='inventoryapp'),
    
    # Materials URLs
    path('material/create/', MaterialCreateView.as_view(), name='material_create'),
    path('material/<int:pk>/', MaterialDetailView.as_view(), name='material_detail'),
    path('material/<int:pk>/edit/', MaterialUpdateView.as_view(), name='material_update'),
    path('material/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material_delete'),
    
    # Inventarios URLs
    path('inventario/create/', InventarioCreateView.as_view(), name='inventario_create'),
    path('inventario/<int:pk>/', InventarioDetailView.as_view(), name='inventario_detail'),
    path('inventario/<int:pk>/edit/', InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventario/<int:pk>/delete/', InventarioDeleteView.as_view(), name='inventario_delete'),
    
    # Inventario-Material URLs
    path('inventario-material/create/', InventarioMaterialCreateView.as_view(), name='inventario_material_create'),
    
    # Proveedores URLs
    path('proveedor/create/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedor/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('proveedor/<int:pk>/edit/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedor/<int:pk>/delete/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
    
    # Proveedor-Material URLs
    path('proveedor-material/create/', ProveedorMaterialCreateView.as_view(), name='proveedor_material_create'),
]