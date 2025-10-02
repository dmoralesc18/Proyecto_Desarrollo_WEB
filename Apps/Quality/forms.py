from django import forms
from .models import Inspeccion, Incidente, Certificacion, PruebaCalidad
from Apps.Projects.models import Proyecto

class InspeccionForm(forms.ModelForm):
    class Meta:
        model = Inspeccion
        fields = ['fecha', 'resultado', 'id_proyecto']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resultado': forms.Select(
                choices=[
                    ('', 'Select result...'),
                    ('Cumple', 'Cumple'),
                    ('No Cumple', 'No Cumple'),
                ],
                attrs={'class': 'form-select'}
            ),
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'fecha': 'Inspection Date',
            'resultado': 'Result',
            'id_proyecto': 'Project',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proyecto'].queryset = Proyecto.objects.all()
        self.fields['id_proyecto'].label_from_instance = lambda obj: f"{obj.nombre_proyecto}"

class IncidenteForm(forms.ModelForm):
    class Meta:
        model = Incidente
        fields = ['descripcion', 'gravedad', 'fecha', 'id_proyecto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the incident...'}),
            'gravedad': forms.Select(
                choices=[
                    ('', 'Select severity...'),
                    ('Baja', 'Baja'),
                    ('Media', 'Media'),
                    ('Alta', 'Alta'),
                    ('Crítica', 'Crítica'),
                ],
                attrs={'class': 'form-select'}
            ),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'descripcion': 'Description',
            'gravedad': 'Severity',
            'fecha': 'Incident Date',
            'id_proyecto': 'Project',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proyecto'].queryset = Proyecto.objects.all()
        self.fields['id_proyecto'].label_from_instance = lambda obj: f"{obj.nombre_proyecto}"

class CertificacionForm(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ['nombre', 'fecha_emision', 'fecha_vencimiento', 'id_proyecto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certification name...'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Certification Name',
            'fecha_emision': 'Issue Date',
            'fecha_vencimiento': 'Expiration Date',
            'id_proyecto': 'Project',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proyecto'].queryset = Proyecto.objects.all()
        self.fields['id_proyecto'].label_from_instance = lambda obj: f"{obj.nombre_proyecto}"

class PruebaCalidadForm(forms.ModelForm):
    class Meta:
        model = PruebaCalidad
        fields = ['tipo', 'resultado', 'fecha', 'id_proyecto']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test type...'}),
            'resultado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test result...'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'tipo': 'Test Type',
            'resultado': 'Result',
            'fecha': 'Test Date',
            'id_proyecto': 'Project',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proyecto'].queryset = Proyecto.objects.all()
        self.fields['id_proyecto'].label_from_instance = lambda obj: f"{obj.nombre_proyecto}"