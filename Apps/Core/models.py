from django.db import models
from django.conf import settings
from Apps.Projects.models import Proyecto

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, db_comment='Administrador/Cliente/Supervisor')
    correo = models.CharField(unique=True, max_length=255)
    contraseña = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'usuario'

class UsuarioProyecto(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_proyecto = models.ForeignKey(Proyecto, models.DO_NOTHING, db_column='id_proyecto')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = getattr(settings, 'DJANGO_MANAGED_MODELS', False)
        db_table = 'usuario_proyecto'
        unique_together = (('id_usuario', 'id_proyecto'),)
