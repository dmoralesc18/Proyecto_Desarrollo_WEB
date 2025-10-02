from django.db import models
from Apps.Projects.models import Proyecto


# Create your models here.

class Subcontratista(models.Model):
    id_subcontratista = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subcontratista'

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    condiciones = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    id_subcontratista = models.ForeignKey('Subcontratista', models.DO_NOTHING, db_column='id_subcontratista')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contrato'