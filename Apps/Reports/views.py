from django.views.generic import TemplateView
from Apps.Core.permissions import AdminOrStaffMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Value, DecimalField, Q, F
from django.utils import timezone
from django.db.utils import OperationalError, ProgrammingError
from django.contrib import messages

from Apps.Finance.models import Factura, Pago
from Apps.Projects.models import Proyecto, Presupuesto
from Apps.Quality.models import Inspeccion, Certificacion
from django.http import HttpResponse
import csv
from django.shortcuts import render

# Create your views here.
class ReportsView(AdminOrStaffMixin, TemplateView):
    template_name = 'reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        decimal_zero = Value(0, output_field=DecimalField(max_digits=14, decimal_places=2))
        # Guardar si no hay tablas todavía
        try:
            _ = Proyecto.objects.count() + Presupuesto.objects.count() + Factura.objects.count() + Pago.objects.count()
            _ = Inspeccion.objects.count() + Certificacion.objects.count()
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Reportes: base de datos sin tablas. Ejecuta migrate y sync_sqlite.')
            today = timezone.now().date()
            next_30 = today + timezone.timedelta(days=30)
            context.update({
                'rep_total_facturado': 0,
                'rep_total_pagado': 0,
                'rep_total_pendiente': 0,
                'rep_proyectos_count': 0,
                'rep_presupuesto_total': 0,
                'rep_inspecciones_cumple': 0,
                'rep_inspecciones_no_cumple': 0,
                'rep_certificaciones_proximas': 0,
                'rep_certificaciones_vencidas': 0,
                'today': today,
                'next_30': next_30,
            })
            return context

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


class ReportAgingView(AdminOrStaffMixin, TemplateView):
    template_name = 'report_aging.html'

    def get_queryset(self, request):
        decimal_zero = Value(0, output_field=DecimalField(max_digits=12, decimal_places=2))
        factura_base = Factura.objects.all()
        pago_base = Pago.objects.all()

        # Filtros
        project_id = request.GET.get('project')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        date_type = request.GET.get('date_type') or 'emision'  # 'emision' | 'pago'
        status = request.GET.get('status')

        if project_id and project_id.isdigit():
            pid = int(project_id)
            factura_base = factura_base.filter(id_proyecto_id=pid)
            pago_base = pago_base.filter(id_factura__id_proyecto_id=pid)

        if status in ["Pendiente", "Pagada"]:
            factura_base = factura_base.filter(estado=status)

        if date_type == 'emision':
            if date_from:
                factura_base = factura_base.filter(fecha_emision__gte=date_from)
                pago_base = pago_base.filter(id_factura__fecha_emision__gte=date_from)
            if date_to:
                factura_base = factura_base.filter(fecha_emision__lte=date_to)
                pago_base = pago_base.filter(id_factura__fecha_emision__lte=date_to)
        elif date_type == 'pago':
            if date_from:
                pago_base = pago_base.filter(fecha__gte=date_from)
            if date_to:
                pago_base = pago_base.filter(fecha__lte=date_to)

        if date_type == 'pago':
            facturas = factura_base.filter(pago__in=pago_base).distinct()
        else:
            facturas = factura_base

        facturas = (
            facturas
            .annotate(
                total_pagado=Coalesce(Sum('pago__monto'), decimal_zero),
                saldo=F('monto') - Coalesce(Sum('pago__monto'), decimal_zero),
            )
            .select_related('id_proyecto')
        )

        # Solo pendientes
        facturas = [f for f in facturas if (f.saldo or 0) > 0]
        return facturas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        facturas = self.get_queryset(request)

        today = timezone.now().date()
        buckets = {
            '0_30': 0.0,
            '31_60': 0.0,
            '61_90': 0.0,
            'gt_90': 0.0,
        }

        table = []
        for f in facturas:
            dias = (today - f.fecha_emision).days if f.fecha_emision else 0
            if dias <= 30:
                bucket = '0-30'
                buckets['0_30'] += float(f.saldo or 0)
            elif dias <= 60:
                bucket = '31-60'
                buckets['31_60'] += float(f.saldo or 0)
            elif dias <= 90:
                bucket = '61-90'
                buckets['61_90'] += float(f.saldo or 0)
            else:
                bucket = '>90'
                buckets['gt_90'] += float(f.saldo or 0)
            table.append({
                'id': f.id_factura,
                'proyecto': getattr(f.id_proyecto, 'nombre_proyecto', ''),
                'fecha_emision': f.fecha_emision,
                'monto': f.monto,
                'pagado': f.total_pagado,
                'saldo': f.saldo,
                'dias': dias,
                'bucket': bucket,
            })

        total_pendiente = sum(float(x['saldo'] or 0) for x in table)

        context.update({
            'projects': Proyecto.objects.all().order_by('nombre_proyecto'),
            'selected_project': request.GET.get('project'),
            'selected_status': request.GET.get('status'),
            'date_type': request.GET.get('date_type') or 'emision',
            'date_from': request.GET.get('date_from'),
            'date_to': request.GET.get('date_to'),
            'aging_rows': table,
            'aging_buckets': buckets,
            'aging_total': total_pendiente,
        })
        # Nombre legible del proyecto seleccionado (si aplica)
        sp = context['selected_project']
        if sp and str(sp).isdigit():
            pr = Proyecto.objects.filter(id_proyecto=int(sp)).first()
            context['selected_project_name'] = getattr(pr, 'nombre_proyecto', None)
        else:
            context['selected_project_name'] = None
        return context

    def render_to_response(self, context, **response_kwargs):
        export = self.request.GET.get('export')
        if export == 'print':
            return render(self.request, 'report_aging_print.html', context)
        if export == 'csv':
            # Exportación CSV de aging
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="aging_facturas.csv"'
            writer = csv.writer(response)
            writer.writerow(['Factura', 'Proyecto', 'Fecha emisión', 'Monto', 'Pagado', 'Saldo', 'Días', 'Bucket'])
            for r in context.get('aging_rows', []):
                writer.writerow([
                    r['id'], r['proyecto'], r['fecha_emision'], r['monto'], r['pagado'], r['saldo'], r['dias'], r['bucket']
                ])
            # Totales por bucket al final
            b = context.get('aging_buckets', {})
            writer.writerow([])
            writer.writerow(['Totales por bucket'])
            writer.writerow(['0-30', b.get('0_30', 0)])
            writer.writerow(['31-60', b.get('31_60', 0)])
            writer.writerow(['61-90', b.get('61_90', 0)])
            writer.writerow(['>90', b.get('gt_90', 0)])
            writer.writerow(['Total pendiente', context.get('aging_total', 0)])
            return response
        return super().render_to_response(context, **response_kwargs)
