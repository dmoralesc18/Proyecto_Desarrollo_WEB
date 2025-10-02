from django import forms
from Apps.Projects.models import Proyecto, Presupuesto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado', 'id_cliente']
        widgets = {
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project name'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Project description'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(
                choices=[
                    ('', 'Select status'),
                    ('Planificación', 'Planning'),
                    ('En Progreso', 'In Progress'),
                    ('Completado', 'Completed'),
                    ('Cancelado', 'Cancelled'),
                    ('En Espera', 'On Hold'),
                ],
                attrs={'class': 'form-control'}
            ),
            'id_cliente': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre_proyecto': 'Project Name',
            'descripcion': 'Description',
            'fecha_inicio': 'Start Date',
            'fecha_fin': 'End Date',
            'estado': 'Status',
            'id_cliente': 'Client',
        }


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['id_proyecto', 'monto_total', 'descripcion']
        widgets = {
            'id_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Total amount'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Budget description'}),
        }
        labels = {
            'id_proyecto': 'Project',
            'monto_total': 'Total Amount',
            'descripcion': 'Description',
        }