from django.urls import path
from .views import (
    FinanceView,
    FacturaCreateView,
    PagoCreateView,
    FacturaListView,
    FacturaUpdateView,
    FacturaDeleteView,
    PagoListView,
    PagoUpdateView,
    PagoDeleteView,
)

urlpatterns = [
   path('', FinanceView.as_view(), name='financeapp'),
   path('invoices/', FacturaListView.as_view(), name='invoice_list'),
   path('invoices/create/', FacturaCreateView.as_view(), name='invoice_create'),
   path('invoices/<int:pk>/edit/', FacturaUpdateView.as_view(), name='invoice_update'),
   path('invoices/<int:pk>/delete/', FacturaDeleteView.as_view(), name='invoice_delete'),
   path('payments/create/', PagoCreateView.as_view(), name='payment_create'),
   path('payments/', PagoListView.as_view(), name='payment_list'),
   path('payments/<int:pk>/edit/', PagoUpdateView.as_view(), name='payment_update'),
   path('payments/<int:pk>/delete/', PagoDeleteView.as_view(), name='payment_delete'),
]
