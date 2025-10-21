from django import forms
from Apps.Equipment.models import MaquinariaEquipo, Alquiler

class MaquinariaEquipoForm(forms.ModelForm):
    class Meta:
        model = MaquinariaEquipo
        fields = ['nombre', 'tipo', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipment name'}),
            'tipo': forms.Select(
                choices=[
                    ('', 'Select type'),
                    ('Propio', 'Owned'),
                    ('Alquilado', 'Rented'),
                ],
                attrs={'class': 'form-control'}
            ),
            'estado': forms.Select(
                choices=[
                    ('', 'Select status'),
                    ('Disponible', 'Available'),
                    ('En Uso', 'In Use'),
                    ('En Mantenimiento', 'Under Maintenance'),
                ],
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'nombre': 'Name',
            'tipo': 'Type',
            'estado': 'Status',
        }


class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['id_equipo', 'id_proyecto', 'fecha_inicio', 'fecha_fin', 'costo']
        widgets = {
            'id_equipo': forms.Select(attrs={'class': 'form-control'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Costo de alquiler'}),
        }
        labels = {
            'id_equipo': 'Equipo',
            'id_proyecto': 'Proyecto',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin',
            'costo': 'Costo de alquiler',
        }