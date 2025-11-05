from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto

# Create your models here.

class Inspeccion(models.Model):
    id_inspeccion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    resultado = models.CharField(max_length=100, blank=True, null=True, db_comment='Cumple/No Cumple')
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'inspeccion'

class Incidente(models.Model):
    id_incidente = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    gravedad = models.CharField(max_length=50, blank=True, null=True, db_comment='Baja/Media/Alta/Cr�tica')
    fecha = models.DateField()
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'incidente'

class Certificacion(models.Model):
    id_certificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'certificacion'

class PruebaCalidad(models.Model):
    id_prueba = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    resultado = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField()
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'prueba_calidad'
