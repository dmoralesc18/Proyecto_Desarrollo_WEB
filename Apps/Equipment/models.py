from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto


# Create your models here.

class MaquinariaEquipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100, blank=True, null=True, db_comment='Propio/Alquilado')
    estado = models.CharField(max_length=50, blank=True, null=True, db_comment='Disponible/En Uso/En Mantenimiento')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'maquinaria_equipo'
    
    def __str__(self):
        return self.nombre

class Alquiler(models.Model):
    id_equipo = models.ForeignKey(MaquinariaEquipo, models.DO_NOTHING, db_column='id_equipo')
    id_alquiler = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    id_equipo = models.ForeignKey('MaquinariaEquipo', models.DO_NOTHING, db_column='id_equipo')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'alquiler'
    
    def __str__(self):
        return f"Rental {self.id_alquiler} - {self.id_equipo.nombre}"
