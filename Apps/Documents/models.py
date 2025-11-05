from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto

# Create your models here.

class DocumentoTecnico(models.Model):
    id_documento = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, blank=True, null=True, db_comment='Plano/Render/Fotograf�a/Informe')
    version = models.CharField(max_length=50, blank=True, null=True)
    fecha_carga = models.DateField()
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'documento_tecnico'
