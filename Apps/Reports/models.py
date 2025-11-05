from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto


# Create your models here.

class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, blank=True, null=True, db_comment='Avance/Financiero/Calidad')
    fecha = models.DateField()
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'reporte'

class Indicador(models.Model):
    id_indicador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_actualizacion = models.DateField()
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'indicador'
