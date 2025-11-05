from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS, ProgrammingError, OperationalError
from django.db import router
from django.apps import apps


class Command(BaseCommand):
    help = "Crea tablas que falten en SQLite para todos los modelos instalados (uso local)"

    def add_arguments(self, parser):
        parser.add_argument('--database', default=DEFAULT_DB_ALIAS, help='Alias de base de datos')

    def handle(self, *args, **options):
        alias = options['database']
        connection = connections[alias]
        if connection.vendor != 'sqlite':
            self.stdout.write(self.style.WARNING('Este comando está pensado sólo para SQLite.'))
        created_total = 0
        # Evitar tocar apps de Django contrib y tablas que ya existen
        skip_apps = {"admin", "auth", "contenttypes", "sessions", "messages", "staticfiles"}
        existing_tables = set(connection.introspection.table_names())
        # Intentar varias rondas para respetar dependencias de FK
        pending = list(apps.get_models(include_auto_created=False))
        for round_idx in range(3):
            created = 0
            still_pending = []
            with connection.schema_editor() as editor:
                for model in pending:
                    app_label = model._meta.app_label
                    if app_label.startswith('django_') or app_label in skip_apps:
                        continue
                    if not router.allow_migrate(alias, model):
                        continue
                    # Saltar si ya existe la tabla
                    tbl = model._meta.db_table
                    if tbl in existing_tables:
                        continue
                    try:
                        editor.create_model(model)
                        created += 1
                        created_total += 1
                        existing_tables.add(tbl)
                        self.stdout.write(self.style.SUCCESS(f"Creada tabla: {model._meta.db_table}"))
                    except (ProgrammingError, OperationalError):
                        # probablemente falta una dependencia; reintentar en la siguiente ronda
                        still_pending.append(model)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"No se pudo crear {model._meta.label}: {e}"))
            pending = still_pending
            if not pending:
                break
        if pending:
            self.stdout.write(self.style.WARNING(f"Tablas no creadas (posibles conflictos): {[m._meta.db_table for m in pending]}"))
        self.stdout.write(self.style.SUCCESS(f"Listo. Tablas creadas: {created_total}"))
