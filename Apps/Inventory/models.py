from django.db import models
from Apps.Projects.models import Proyecto


# Create your models here.

class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    unidad = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material'

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'

class InventarioMaterial(models.Model):
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    id_material = models.ForeignKey('Material', models.DO_NOTHING, db_column='id_material')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_material'
        unique_together = (('id_inventario', 'id_material'),)

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'

class ProveedorMaterial(models.Model):
    id_proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='id_proveedor')
    id_material = models.ForeignKey(Material, models.DO_NOTHING, db_column='id_material')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tiempo_entrega = models.IntegerField(blank=True, null=True, db_comment='Días de entrega')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor_material'
        unique_together = (('id_proveedor', 'id_material'),)
