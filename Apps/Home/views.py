from django.shortcuts import render
from django.views.generic import TemplateView

# Model imports for dashboard counts
try:
    from Apps.Projects.models import Proyecto
    from Apps.Quality.models import Inspeccion, Incidente, Certificacion, PruebaCalidad
    from Apps.Subcontractors.models import Subcontratista
    from Apps.Clients.models import Cliente
    from Apps.Documents.models import DocumentoTecnico
    from Apps.Equipment.models import MaquinariaEquipo
    from Apps.Finance.models import Factura, Pago
    from Apps.Inventory.models import Inventario, Material, Proveedor
    from Apps.Reports.models import Reporte
except Exception:  # pragma: no cover - tolerate import issues in migrations/setup
    Proyecto = Inspeccion = Incidente = Certificacion = PruebaCalidad = Subcontratista = Cliente = DocumentoTecnico = MaquinariaEquipo = Factura = Pago = Inventario = Material = Proveedor = Reporte = None

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        def safe_count(model):
            try:
                return model.objects.count() if model is not None else 0
            except Exception:
                return 0

        # Totales simples
        counts = {
            'projects': safe_count(Proyecto),
            'quality': safe_count(Inspeccion),
            'subcontractors': safe_count(Subcontratista),
            'clients': safe_count(Cliente),
            'documents': safe_count(DocumentoTecnico),
            'equipment': safe_count(MaquinariaEquipo),
            'finance_invoices': safe_count(Factura),
            'finance_payments': safe_count(Pago),
            'inventory': safe_count(Inventario),
            'reports': safe_count(Reporte),
        }
        context['counts'] = counts

        # Resumen detallado (filtrados seguros con try/except por si faltan columnas)
        summary = {}

        # Proyectos por estado (común: Activo/Finalizado)
        proj_active = proj_finished = 0
        try:
            proj_active = Proyecto.objects.filter(estado__iexact='Activo').count()
            proj_finished = Proyecto.objects.filter(estado__iexact='Finalizado').count()
        except Exception:
            pass
        summary['projects'] = {
            'total': counts['projects'],
            'active': proj_active,
            'finished': proj_finished,
        }

        # Calidad: inspecciones, incidentes, certificaciones, pruebas
        def safe_filter_count(model, **kwargs):
            try:
                return model.objects.filter(**kwargs).count() if model is not None else 0
            except Exception:
                return 0
        summary['quality'] = {
            'inspections': counts['quality'],
            'incidents': safe_count(Incidente),
            'certifications': safe_count(Certificacion),
            'tests': safe_count(PruebaCalidad),
        }

        # Subcontratistas
        summary['subcontractors'] = {'total': counts['subcontractors']}

        # Clientes
        summary['clients'] = {'total': counts['clients']}

        # Documentos por tipo (si aplica)
        docs_plano = docs_render = docs_informe = 0
        try:
            docs_plano = DocumentoTecnico.objects.filter(tipo__iexact='Plano').count()
            docs_render = DocumentoTecnico.objects.filter(tipo__iexact='Render').count()
            # Fotografía puede tener acentos distintos; usamos icontains
            docs_foto = DocumentoTecnico.objects.filter(tipo__icontains='foto').count()
            docs_informe = DocumentoTecnico.objects.filter(tipo__iexact='Informe').count()
        except Exception:
            docs_foto = 0
        summary['documents'] = {
            'total': counts['documents'],
            'planos': docs_plano,
            'renders': docs_render,
            'fotos': docs_foto,
            'informes': docs_informe,
        }

        # Equipos por estado
        eq_disponible = eq_uso = eq_mant = 0
        try:
            eq_disponible = MaquinariaEquipo.objects.filter(estado__iexact='Disponible').count()
            eq_uso = MaquinariaEquipo.objects.filter(estado__iexact='En Uso').count()
            eq_mant = MaquinariaEquipo.objects.filter(estado__icontains='Manten').count()
        except Exception:
            pass
        summary['equipment'] = {
            'total': counts['equipment'],
            'available': eq_disponible,
            'in_use': eq_uso,
            'maintenance': eq_mant,
        }

        # Finanzas por estado de factura
        inv_paid = inv_pending = 0
        try:
            inv_paid = Factura.objects.filter(estado__iexact='Pagada').count()
            inv_pending = Factura.objects.filter(estado__iexact='Pendiente').count()
        except Exception:
            pass
        summary['finance'] = {
            'invoices_total': counts['finance_invoices'],
            'invoices_paid': inv_paid,
            'invoices_pending': inv_pending,
            'payments_total': counts['finance_payments'],
        }

        # Inventario: almacenes, materiales, proveedores
        summary['inventory'] = {
            'stores': counts['inventory'],
            'materials': safe_count(Material),
            'providers': safe_count(Proveedor),
        }

        # Reportes
        summary['reports'] = {
            'total': counts['reports']
        }

        context['summary'] = summary
        return context
