from django import forms

from Apps.Finance.models import Factura, Pago, FacturaMeta, PagoMeta
from Apps.Projects.models import Proyecto
from Apps.Inventory.models import Proveedor
from Apps.Subcontractors.models import Subcontratista


class FacturaForm(forms.ModelForm):
    descripcion = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    origen_tipo = forms.ChoiceField(label='Generado por', required=False, choices=(('proveedor', 'Proveedor'), ('subcontratista', 'Subcontratista')), widget=forms.Select(attrs={'class': 'form-select'}))
    proveedor = forms.ModelChoiceField(label='Proveedor', required=False, queryset=Proveedor.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    subcontratista = forms.ModelChoiceField(label='Subcontratista', required=False, queryset=Subcontratista.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = Factura
        fields = [
            'id_proyecto',
            'monto',
            'fecha_emision',
            'estado',
        ]
        widgets = {
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(choices=(('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')), attrs={'class': 'form-select'}),
        }
        labels = {
            'id_proyecto': 'Proyecto',
            'monto': 'Monto (Q)',
            'fecha_emision': 'Fecha de emisión',
            'estado': 'Estado',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, precargar metadatos
        instance = kwargs.get('instance')
        if instance and hasattr(instance, 'meta'):
            self.fields['descripcion'].initial = instance.meta.descripcion
            self.fields['origen_tipo'].initial = instance.meta.origen_tipo
            self.fields['proveedor'].initial = instance.meta.proveedor_id
            self.fields['subcontratista'].initial = instance.meta.subcontratista_id


class PagoForm(forms.ModelForm):
    descripcion = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    origen_tipo = forms.ChoiceField(label='Generado por', required=False, choices=(('proveedor', 'Proveedor'), ('subcontratista', 'Subcontratista')), widget=forms.Select(attrs={'class': 'form-select'}))
    proveedor = forms.ModelChoiceField(label='Proveedor', required=False, queryset=Proveedor.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    subcontratista = forms.ModelChoiceField(label='Subcontratista', required=False, queryset=Subcontratista.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = Pago
        fields = [
            'id_factura',
            'monto',
            'fecha',
            'metodo_pago',
        ]
        widgets = {
            'id_factura': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transferencia, efectivo, etc.'}),
        }
        labels = {
            'id_factura': 'Factura',
            'monto': 'Monto (Q)',
            'fecha': 'Fecha de pago',
            'metodo_pago': 'Método de pago',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar y optimizar consulta de facturas
        self.fields['id_factura'].queryset = (
            Factura.objects.select_related('id_proyecto').order_by('-fecha_emision', '-id_factura')
        )
        # Mostrar etiqueta clara para cada factura
        def label_from_instance(obj: Factura):
            proyecto = getattr(obj.id_proyecto, 'nombre_proyecto', '') if obj.id_proyecto_id else ''
            estado = obj.estado or '-'
            return f"#{obj.id_factura} · {proyecto} · {obj.fecha_emision} · Q{obj.monto} ({estado})"
        self.fields['id_factura'].label_from_instance = label_from_instance
        # Si estamos editando, precargar metadatos
        instance = kwargs.get('instance')
        if instance and hasattr(instance, 'meta'):
            self.fields['descripcion'].initial = instance.meta.descripcion
            self.fields['origen_tipo'].initial = instance.meta.origen_tipo
            self.fields['proveedor'].initial = instance.meta.proveedor_id
            self.fields['subcontratista'].initial = instance.meta.subcontratista_id
