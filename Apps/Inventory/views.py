from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.utils import OperationalError, ProgrammingError
from Apps.Core.permissions import AdminOnlyMixin, AdminOrStaffMixin
from Apps.Inventory.models import Material, Inventario, InventarioMaterial, Proveedor, ProveedorMaterial
from .forms import MaterialForm, InventarioForm, InventarioMaterialForm, ProveedorForm, ProveedorMaterialForm

# ============================================
# VISTA PRINCIPAL DE INVENTARIO
# ============================================

class InventoryView(AdminOrStaffMixin, ListView):
    model = Material
    template_name = 'inventory.html'
    context_object_name = 'materiales'
    
    def get_queryset(self):
        qs = Material.objects.all()
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'La base de datos no tiene tablas de Inventario aún. Ejecuta migrate y sync_sqlite.')
            return Material.objects.none()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['inventarios'] = Inventario.objects.all()
        except (OperationalError, ProgrammingError):
            context['inventarios'] = Inventario.objects.none()
        try:
            context['proveedores'] = Proveedor.objects.all()
        except (OperationalError, ProgrammingError):
            context['proveedores'] = Proveedor.objects.none()
        return context


# ============================================
# VISTAS DE MATERIAL
# ============================================

class MaterialDetailView(AdminOrStaffMixin, DetailView):
    model = Material
    template_name = 'material_detail.html'
    context_object_name = 'material'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedores_material'] = ProveedorMaterial.objects.filter(id_material=self.object)
        context['inventarios_material'] = InventarioMaterial.objects.filter(id_material=self.object)
        return context

class MaterialCreateView(AdminOrStaffMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'material_form.html'
    success_url = reverse_lazy('inventoryapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Material'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Material created successfully.')
        return super().form_valid(form)

class MaterialUpdateView(AdminOnlyMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'material_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Material'
        return context
    
    def get_success_url(self):
        return reverse_lazy('material_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Material updated successfully.')
        return super().form_valid(form)

class MaterialDeleteView(AdminOnlyMixin, DeleteView):
    model = Material
    template_name = 'material_delete.html'
    context_object_name = 'material'
    success_url = reverse_lazy('inventoryapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Material deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE INVENTARIO
# ============================================

class InventarioDetailView(AdminOrStaffMixin, DetailView):
    model = Inventario
    template_name = 'inventario_detail.html'
    context_object_name = 'inventario'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materiales_inventario'] = InventarioMaterial.objects.filter(id_inventario=self.object)
        return context

class InventarioCreateView(AdminOrStaffMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventario_form.html'
    success_url = reverse_lazy('inventoryapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Inventory'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Inventory created successfully.')
        return super().form_valid(form)

class InventarioUpdateView(AdminOnlyMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'inventario_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Inventory'
        return context
    
    def get_success_url(self):
        return reverse_lazy('inventario_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Inventory updated successfully.')
        return super().form_valid(form)

class InventarioDeleteView(AdminOnlyMixin, DeleteView):
    model = Inventario
    template_name = 'inventario_delete.html'
    context_object_name = 'inventario'
    success_url = reverse_lazy('inventoryapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Inventory deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE INVENTARIO-MATERIAL
# ============================================

class InventarioMaterialCreateView(AdminOrStaffMixin, CreateView):
    model = InventarioMaterial
    form_class = InventarioMaterialForm
    template_name = 'inventario_material_form.html'
    success_url = reverse_lazy('inventoryapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Add Material to Inventory'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Material added to inventory successfully.')
        return super().form_valid(form)


# ============================================
# VISTAS DE PROVEEDOR
# ============================================

class ProveedorDetailView(AdminOrStaffMixin, DetailView):
    model = Proveedor
    template_name = 'proveedor_detail.html'
    context_object_name = 'proveedor'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materiales_proveedor'] = ProveedorMaterial.objects.filter(id_proveedor=self.object)
        return context

class ProveedorCreateView(AdminOrStaffMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_form.html'
    success_url = reverse_lazy('inventoryapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'New Supplier'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Supplier created successfully.')
        return super().form_valid(form)

class ProveedorUpdateView(AdminOnlyMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_form.html'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Edit Supplier'
        return context
    
    def get_success_url(self):
        return reverse_lazy('proveedor_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Supplier updated successfully.')
        return super().form_valid(form)

class ProveedorDeleteView(AdminOnlyMixin, DeleteView):
    model = Proveedor
    template_name = 'proveedor_delete.html'
    context_object_name = 'proveedor'
    success_url = reverse_lazy('inventoryapp')
    pk_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Supplier deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================
# VISTAS DE PROVEEDOR-MATERIAL
# ============================================

class ProveedorMaterialCreateView(AdminOrStaffMixin, CreateView):
    model = ProveedorMaterial
    form_class = ProveedorMaterialForm
    template_name = 'proveedor_material_form.html'
    success_url = reverse_lazy('inventoryapp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Add Material to Supplier'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Material added to supplier successfully.')
        return super().form_valid(form)
