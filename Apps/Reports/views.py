from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Value, DecimalField, Q, F
from django.utils import timezone

from Apps.Finance.models import Factura, Pago
from Apps.Projects.models import Proyecto, Presupuesto
from Apps.Quality.models import Inspeccion, Certificacion

# Create your views here.
class ReportsView(TemplateView):
    template_name = 'reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        decimal_zero = Value(0, output_field=DecimalField(max_digits=14, decimal_places=2))

        # Finanzas (globales)
        total_facturado = Factura.objects.aggregate(
            total=Coalesce(Sum('monto'), decimal_zero)
        )['total']

        total_pagado = Pago.objects.aggregate(
            total=Coalesce(Sum('monto'), decimal_zero)
        )['total']

        total_pendiente = (
            Factura.objects
            .annotate(pagado=Coalesce(Sum('pago__monto'), decimal_zero))
            .annotate(saldo=F('monto') - Coalesce(Sum('pago__monto'), decimal_zero))
            .aggregate(total=Coalesce(Sum('saldo'), decimal_zero))['total']
        )

        # Proyectos
        proyectos_count = Proyecto.objects.count()
        presupuesto_total = Presupuesto.objects.aggregate(
            total=Coalesce(Sum('monto_total'), decimal_zero)
        )['total']

        # Calidad
        cumple_count = Inspeccion.objects.filter(resultado='Cumple').count()
        no_cumple_count = Inspeccion.objects.filter(resultado='No Cumple').count()

        today = timezone.now().date()
        next_30 = today + timezone.timedelta(days=30)
        certificaciones_proximas = Certificacion.objects.filter(
            fecha_vencimiento__isnull=False,
            fecha_vencimiento__gte=today,
            fecha_vencimiento__lte=next_30,
        ).count()
        certificaciones_vencidas = Certificacion.objects.filter(
            fecha_vencimiento__isnull=False,
            fecha_vencimiento__lt=today,
        ).count()

        context.update({
            # Finanzas
            'rep_total_facturado': total_facturado,
            'rep_total_pagado': total_pagado,
            'rep_total_pendiente': total_pendiente,
            # Proyectos
            'rep_proyectos_count': proyectos_count,
            'rep_presupuesto_total': presupuesto_total,
            # Calidad
            'rep_inspecciones_cumple': cumple_count,
            'rep_inspecciones_no_cumple': no_cumple_count,
            'rep_certificaciones_proximas': certificaciones_proximas,
            'rep_certificaciones_vencidas': certificaciones_vencidas,
            'today': today,
            'next_30': next_30,
        })

        return context
