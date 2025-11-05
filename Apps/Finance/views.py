from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from Apps.Core.permissions import AdminOnlyMixin
from django.db.models import Sum, F, Value, DecimalField, Q
from django.db.models.functions import Coalesce
from django.db.utils import OperationalError, ProgrammingError
from django.contrib import messages

from Apps.Finance.models import Factura, Pago
from Apps.Projects.models import Proyecto
from Apps.Finance.forms import FacturaForm, PagoForm
from django.urls import reverse_lazy
from Apps.Finance.models import FacturaMeta, PagoMeta

# Create your views here.
class FinanceView(AdminOnlyMixin, TemplateView):
    template_name = 'finance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        decimal_zero = Value(0, output_field=DecimalField(max_digits=12, decimal_places=2))
        # Early guard: si las tablas no existen aún en SQLite, evita romper y muestra aviso
        try:
            # Fuerza consultas mínimas
            _ = Proyecto.objects.count() + Factura.objects.count() + Pago.objects.count()
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Finanzas: base de datos sin tablas. Ejecuta migrate y sync_sqlite.')
            context.update({
                'projects': [],
                'selected_project': None,
                'selected_status': None,
                'date_type': 'emision',
                'date_from': None,
                'date_to': None,
                'invoices_pending': [],
                'summary_projects': [],
            })
            return context

        # Filtros
        projects_qs = Proyecto.objects.all().order_by('nombre_proyecto')
        project_id = self.request.GET.get('project')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        date_type = self.request.GET.get('date_type') or 'emision'  # 'emision' | 'pago'
        status = self.request.GET.get('status')  # 'Pendiente', 'Pagada' o None

        factura_base = Factura.objects.all()
        pago_base = Pago.objects.all()
        proyecto_base = Proyecto.objects.all()

        if project_id:
            try:
                project_id_int = int(project_id)
                factura_base = factura_base.filter(id_proyecto_id=project_id_int)
                pago_base = pago_base.filter(id_factura__id_proyecto_id=project_id_int)
                proyecto_base = proyecto_base.filter(id_proyecto=project_id_int)
            except ValueError:
                project_id_int = None
        else:
            project_id_int = None

        # Filtro por estado de factura
        if status in ["Pendiente", "Pagada"]:
            factura_base = factura_base.filter(estado=status)
            selected_status = status
        else:
            selected_status = None

        # Filtro por rango de fechas, según tipo seleccionado
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

        # Determinar conjunto de facturas según tipo de fecha
        if date_type == 'pago':
            facturas_in_range = factura_base.filter(pago__in=pago_base).distinct()
        else:
            facturas_in_range = factura_base

        # Facturas con saldo pendiente (monto facturado - monto pagado > 0)
        if date_type == 'pago':
            pago_cutoff_q = Q()
            if date_to:
                pago_cutoff_q &= Q(pago__fecha__lte=date_to)
            if selected_status:
                pago_cutoff_q &= Q(estado=selected_status)
            facturas_con_saldo = (
                facturas_in_range
                .annotate(
                    total_pagado=Coalesce(Sum('pago__monto', filter=pago_cutoff_q), decimal_zero),
                    saldo=F('monto') - Coalesce(Sum('pago__monto', filter=pago_cutoff_q), decimal_zero),
                )
                .filter(saldo__gt=0)
                .select_related('id_proyecto')
            )
        else:
            facturas_con_saldo = (
                factura_base
                .annotate(
                    total_pagado=Coalesce(Sum('pago__monto'), decimal_zero),
                    saldo=F('monto') - Coalesce(Sum('pago__monto'), decimal_zero),
                )
                .filter(saldo__gt=0)
                .select_related('id_proyecto')
            )

        # Resumen por proyecto: total facturado, total pagado y presupuesto (si existe)
        if date_type == 'pago':
            resumen_proyectos = (
                proyecto_base
                .annotate(
                    total_facturado=Coalesce(
                        Sum('factura__monto', filter=Q(factura__in=facturas_in_range)),
                        decimal_zero,
                    ),
                    total_pagado=Coalesce(
                        Sum('factura__pago__monto', filter=Q(factura__pago__in=pago_base)),
                        decimal_zero,
                    ),
                    total_pagado_cutoff=Coalesce(
                        Sum('factura__pago__monto', filter=(Q() if not date_to else Q(factura__pago__fecha__lte=date_to)) & (Q() if not selected_status else Q(factura__estado=selected_status))),
                        decimal_zero,
                    ),
                    presupuesto_agg=Coalesce(Sum('presupuesto__monto_total'), decimal_zero),
                )
                .order_by('nombre_proyecto')
            )
        else:
            resumen_proyectos = (
                proyecto_base
                .annotate(
                    total_facturado=Coalesce(Sum('factura__monto'), decimal_zero),
                    total_pagado=Coalesce(Sum('factura__pago__monto'), decimal_zero),
                    presupuesto_agg=Coalesce(Sum('presupuesto__monto_total'), decimal_zero),
                )
                .order_by('nombre_proyecto')
            )
        # Convertimos a lista para calcular campos derivados sin perder el queryset base
        resumen_proyectos_list = list(resumen_proyectos)
        for p in resumen_proyectos_list:
            fact = p.total_facturado or 0
            pag = p.total_pagado or 0
            pres = p.presupuesto_agg or 0
            # En modo pago, el saldo y presupuesto restante se calculan con pagos hasta el corte
            if date_type == 'pago':
                pag_corte = getattr(p, 'total_pagado_cutoff', None) or 0
                p.pendiente_facturas = fact - pag_corte
                p.presupuesto_restante_proyecto = pres - pag_corte
            else:
                p.pendiente_facturas = fact - pag
                p.presupuesto_restante_proyecto = pres - pag
            p.presupuesto_total_proyecto = pres

        # Totales (alcance actual del filtro)
        total_pagado_global = pago_base.aggregate(
            total=Coalesce(Sum('monto'), decimal_zero)
        )['total']

        if date_type == 'pago':
            total_facturado_global = facturas_in_range.aggregate(
                total=Coalesce(Sum('monto'), decimal_zero)
            )['total']

            pago_cutoff_q = Q()
            if date_to:
                pago_cutoff_q &= Q(pago__fecha__lte=date_to)
            if selected_status:
                pago_cutoff_q &= Q(estado=selected_status)
            total_pendiente_global = (
                facturas_in_range
                .annotate(
                    pagado=Coalesce(Sum('pago__monto', filter=pago_cutoff_q), decimal_zero),
                    saldo=F('monto') - Coalesce(Sum('pago__monto', filter=pago_cutoff_q), decimal_zero),
                )
                .aggregate(total=Coalesce(Sum('saldo'), decimal_zero))['total']
            )
        else:
            total_facturado_global = factura_base.aggregate(
                total=Coalesce(Sum('monto'), decimal_zero)
            )['total']

            total_pendiente_global = (
                factura_base
                .annotate(
                    pagado=Coalesce(Sum('pago__monto'), decimal_zero),
                    saldo=F('monto') - Coalesce(Sum('pago__monto'), decimal_zero),
                )
                .aggregate(total=Coalesce(Sum('saldo'), decimal_zero))['total']
            )

        # Presupuesto agregado y restante en el alcance
        presupuesto_total = proyecto_base.aggregate(
            total=Coalesce(Sum('presupuesto__monto_total'), decimal_zero)
        )['total']
        presupuesto_restante = (presupuesto_total or 0) - (total_pagado_global or 0)
        if presupuesto_restante is None:
            presupuesto_restante = 0
        # KPI de porcentaje pagado
        if (total_facturado_global or 0) > 0:
            pct_pagado = float(total_pagado_global) / float(total_facturado_global) * 100.0
        else:
            pct_pagado = 0.0

        # Datos para gráficos simples (por proyecto)
        labels = []
        serie_pagado = []
        serie_pendiente = []
        for p in resumen_proyectos:
            labels.append(p.nombre_proyecto)
            pagado = p.total_pagado or 0
            pendiente = (p.total_facturado or 0) - (p.total_pagado or 0)
            serie_pagado.append(float(pagado))
            serie_pendiente.append(float(pendiente))

        context.update({
            'projects': projects_qs,
            'selected_project': project_id_int,
            'selected_status': selected_status,
            'date_type': date_type,
            'date_from': date_from,
            'date_to': date_to,
            'facturas_pendientes': facturas_con_saldo,
            'resumen_proyectos': resumen_proyectos_list,
            'total_facturado_global': total_facturado_global,
            'total_pagado_global': total_pagado_global,
            'total_pendiente_global': total_pendiente_global,
            'presupuesto_total': presupuesto_total,
            'presupuesto_restante': presupuesto_restante,
            'pct_pagado': pct_pagado,
            'chart_labels': labels,
            'chart_pagado': serie_pagado,
            'chart_pendiente': serie_pendiente,
            'has_totals_data': bool((total_pagado_global or 0) or (total_pendiente_global or 0)),
            'has_projects_data': bool(labels),
        })
        return context


class FacturaCreateView(AdminOnlyMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura_form.html'
    success_url = reverse_lazy('financeapp')

    def form_valid(self, form):
        response = super().form_valid(form)
        descripcion = form.cleaned_data.get('descripcion')
        origen_tipo = form.cleaned_data.get('origen_tipo')
        proveedor = form.cleaned_data.get('proveedor')
        subcontratista = form.cleaned_data.get('subcontratista')
        FacturaMeta.objects.update_or_create(
            factura=self.object,
            defaults={
                'descripcion': descripcion,
                'origen_tipo': origen_tipo,
                'proveedor': proveedor if origen_tipo == 'proveedor' else None,
                'subcontratista': subcontratista if origen_tipo == 'subcontratista' else None,
            }
        )
        return response


class PagoCreateView(AdminOnlyMixin, CreateView):
    model = Pago
    form_class = PagoForm
    template_name = 'pago_form.html'
    success_url = reverse_lazy('financeapp')

    def get_initial(self):
        initial = super().get_initial()
        invoice_id = self.request.GET.get('invoice')
        if invoice_id and invoice_id.isdigit():
            initial['id_factura'] = int(invoice_id)
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        descripcion = form.cleaned_data.get('descripcion')
        origen_tipo = form.cleaned_data.get('origen_tipo')
        proveedor = form.cleaned_data.get('proveedor')
        subcontratista = form.cleaned_data.get('subcontratista')
        PagoMeta.objects.update_or_create(
            pago=self.object,
            defaults={
                'descripcion': descripcion,
                'origen_tipo': origen_tipo,
                'proveedor': proveedor if origen_tipo == 'proveedor' else None,
                'subcontratista': subcontratista if origen_tipo == 'subcontratista' else None,
            }
        )
        return response


class FacturaListView(AdminOnlyMixin, ListView):
    model = Factura
    template_name = 'factura_list.html'
    context_object_name = 'facturas'
    paginate_by = 20
    def get_queryset(self):
        qs = Factura.objects.all()
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Finanzas: la tabla de facturas no existe aún.')
            return Factura.objects.none()
        return qs


class FacturaUpdateView(AdminOnlyMixin, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'factura_form.html'
    success_url = reverse_lazy('invoice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        descripcion = form.cleaned_data.get('descripcion')
        origen_tipo = form.cleaned_data.get('origen_tipo')
        proveedor = form.cleaned_data.get('proveedor')
        subcontratista = form.cleaned_data.get('subcontratista')
        FacturaMeta.objects.update_or_create(
            factura=self.object,
            defaults={
                'descripcion': descripcion,
                'origen_tipo': origen_tipo,
                'proveedor': proveedor if origen_tipo == 'proveedor' else None,
                'subcontratista': subcontratista if origen_tipo == 'subcontratista' else None,
            }
        )
        return response


class FacturaDeleteView(AdminOnlyMixin, DeleteView):
    model = Factura
    template_name = 'factura_delete.html'
    success_url = reverse_lazy('invoice_list')


class PagoListView(AdminOnlyMixin, ListView):
    model = Pago
    template_name = 'pago_list.html'
    context_object_name = 'pagos'
    paginate_by = 20
    def get_queryset(self):
        qs = Pago.objects.all()
        try:
            list(qs[:1])
        except (OperationalError, ProgrammingError):
            messages.warning(self.request, 'Finanzas: la tabla de pagos no existe aún.')
            return Pago.objects.none()
        return qs


class PagoUpdateView(AdminOnlyMixin, UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'pago_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        descripcion = form.cleaned_data.get('descripcion')
        origen_tipo = form.cleaned_data.get('origen_tipo')
        proveedor = form.cleaned_data.get('proveedor')
        subcontratista = form.cleaned_data.get('subcontratista')
        PagoMeta.objects.update_or_create(
            pago=self.object,
            defaults={
                'descripcion': descripcion,
                'origen_tipo': origen_tipo,
                'proveedor': proveedor if origen_tipo == 'proveedor' else None,
                'subcontratista': subcontratista if origen_tipo == 'subcontratista' else None,
            }
        )
        return response


class PagoDeleteView(AdminOnlyMixin, DeleteView):
    model = Pago
    template_name = 'pago_delete.html'
    success_url = reverse_lazy('payment_list')
