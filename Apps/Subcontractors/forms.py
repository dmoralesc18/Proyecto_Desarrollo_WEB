from django import forms
from Apps.Subcontractors.models import Subcontratista, Contrato

class SubcontratistaForm(forms.ModelForm):
    class Meta:
        model = Subcontratista
        fields = ['nombre', 'especialidad', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcontractor name'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialty'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact (phone/email)'}),
        }
        labels = {
            'nombre': 'Name',
            'especialidad': 'Specialty',
            'contacto': 'Contact',
        }


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['id_subcontratista', 'id_proyecto', 'condiciones', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'id_subcontratista': forms.Select(attrs={'class': 'form-control'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'condiciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Contract conditions'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'id_subcontratista': 'Subcontractor',
            'id_proyecto': 'Project',
            'condiciones': 'Conditions',
            'fecha_inicio': 'Start Date',
            'fecha_fin': 'End Date',
        }