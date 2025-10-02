from django.db import models
from Apps.Projects.models import Proyecto

# Create your models here.

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_emision = models.DateField()
    estado = models.CharField(max_length=50, blank=True, null=True, db_comment='Pagada/Pendiente')
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factura'

class Pago(models.Model):
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pago'
