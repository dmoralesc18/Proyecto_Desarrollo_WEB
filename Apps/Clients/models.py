from django.db import models
from django.conf import settings

# Create your models here.

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cliente = models.CharField(max_length=255)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'cliente'

    def __str__(self):
        return self.nombre_cliente
