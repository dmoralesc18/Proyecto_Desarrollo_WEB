from django import forms
from Apps.Inventory.models import Material, Inventario, InventarioMaterial, Proveedor, ProveedorMaterial

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'unidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Material name'}),
            'unidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (kg, m, pcs, etc.)'}),
        }
        labels = {
            'nombre': 'Name',
            'unidad': 'Unit',
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['id_proyecto', 'ubicacion']
        widgets = {
            'id_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }
        labels = {
            'id_proyecto': 'Project',
            'ubicacion': 'Location',
        }


class InventarioMaterialForm(forms.ModelForm):
    class Meta:
        model = InventarioMaterial
        fields = ['id_inventario', 'id_material', 'cantidad']
        widgets = {
            'id_inventario': forms.Select(attrs={'class': 'form-control'}),
            'id_material': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Quantity'}),
        }
        labels = {
            'id_inventario': 'Inventory',
            'id_material': 'Material',
            'cantidad': 'Quantity',
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier name'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact (phone/email)'}),
        }
        labels = {
            'nombre': 'Name',
            'contacto': 'Contact',
        }


class ProveedorMaterialForm(forms.ModelForm):
    class Meta:
        model = ProveedorMaterial
        fields = ['id_proveedor', 'id_material', 'precio_unitario', 'tiempo_entrega']
        widgets = {
            'id_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'id_material': forms.Select(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Unit price'}),
            'tiempo_entrega': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Delivery days'}),
        }
        labels = {
            'id_proveedor': 'Supplier',
            'id_material': 'Material',
            'precio_unitario': 'Unit Price',
            'tiempo_entrega': 'Delivery Time (days)',
        }