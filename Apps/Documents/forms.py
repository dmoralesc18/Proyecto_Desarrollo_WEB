from django import forms
from .models import DocumentoTecnico
from Apps.Projects.models import Proyecto

class DocumentoTecnicoForm(forms.ModelForm):
    class Meta:
        model = DocumentoTecnico
        fields = ['tipo', 'version', 'fecha_carga', 'id_proyecto']
        widgets = {
            'tipo': forms.Select(
                choices=[
                    ('', 'Select type...'),
                    ('Plano', 'Plano'),
                    ('Render', 'Render'),
                    ('Fotografía', 'Fotografía'),
                    ('Informe', 'Informe'),
                ],
                attrs={'class': 'form-select'}
            ),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., v1.0'}),
            'fecha_carga': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_proyecto': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'tipo': 'Document Type',
            'version': 'Version',
            'fecha_carga': 'Upload Date',
            'id_proyecto': 'Project',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proyecto'].queryset = Proyecto.objects.all()
        self.fields['id_proyecto'].label_from_instance = lambda obj: f"{obj.nombre_proyecto}"