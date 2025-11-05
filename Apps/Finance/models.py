from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto
from Apps.Inventory.models import Proveedor
from Apps.Subcontractors.models import Subcontratista

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
        managed = True
        db_table = 'factura'

    def __str__(self):
        proyecto = getattr(self.id_proyecto, 'nombre_proyecto', '') if self.id_proyecto_id else ''
        estado = self.estado or '-'
        return f"Factura #{self.id_factura} - {proyecto} - {self.fecha_emision} - Q{self.monto} ({estado})"

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
        managed = True
        db_table = 'pago'

    def __str__(self):
        return f"Pago #{self.id_pago} - Q{self.monto} - {self.fecha}"


# Campos adicionales (metadatos) para Factura y Pago
class FacturaMeta(models.Model):
    ORIGEN_CHOICES = (
        ('proveedor', 'Proveedor'),
        ('subcontratista', 'Subcontratista'),
    )

    factura = models.OneToOneField(Factura, on_delete=models.CASCADE, related_name='meta')
    descripcion = models.TextField(blank=True, null=True)
    origen_tipo = models.CharField(max_length=20, choices=ORIGEN_CHOICES, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, models.SET_NULL, blank=True, null=True)
    subcontratista = models.ForeignKey(Subcontratista, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'factura_meta'

    def __str__(self):
        return f"Meta Factura #{self.factura_id}"


class PagoMeta(models.Model):
    ORIGEN_CHOICES = (
        ('proveedor', 'Proveedor'),
        ('subcontratista', 'Subcontratista'),
    )

    pago = models.OneToOneField(Pago, on_delete=models.CASCADE, related_name='meta')
    descripcion = models.TextField(blank=True, null=True)
    origen_tipo = models.CharField(max_length=20, choices=ORIGEN_CHOICES, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, models.SET_NULL, blank=True, null=True)
    subcontratista = models.ForeignKey(Subcontratista, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pago_meta'

    def __str__(self):
        return f"Meta Pago #{self.pago_id}"
