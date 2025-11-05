from django.db import migrations


def create_projects_sqlite(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            r"""
            CREATE TABLE IF NOT EXISTS proyecto (
                id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_proyecto VARCHAR(255) NOT NULL,
                descripcion TEXT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE,
                estado VARCHAR(50),
                id_cliente INTEGER NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
            );
            """
        )
        cursor.execute(
            r"""
            CREATE TABLE IF NOT EXISTS presupuesto (
                id_presupuesto INTEGER PRIMARY KEY AUTOINCREMENT,
                monto_total DECIMAL(12,2) NOT NULL,
                descripcion TEXT,
                id_proyecto INTEGER NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(id_proyecto) REFERENCES proyecto(id_proyecto)
            );
            """
        )


class Migration(migrations.Migration):
    dependencies = [
        ('Projects', '0001_initial'),
        ('Clients', '0002_create_cliente_sqlite'),
    ]

    operations = [
        migrations.RunPython(create_projects_sqlite, migrations.RunPython.noop),
    ]
