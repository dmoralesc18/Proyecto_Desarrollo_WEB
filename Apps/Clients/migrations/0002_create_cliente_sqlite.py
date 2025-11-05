from django.db import migrations


def create_cliente_sqlite(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            r"""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_cliente VARCHAR(255) NOT NULL,
                contacto VARCHAR(100),
                direccion VARCHAR(255),
                created_at DATETIME,
                updated_at DATETIME
            );
            """
        )


class Migration(migrations.Migration):
    dependencies = [
        ('Clients', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_cliente_sqlite, migrations.RunPython.noop),
    ]
