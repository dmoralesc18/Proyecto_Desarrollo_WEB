from django.contrib import admin
from django.urls import path, include
from Apps.Reports import views
from .views import ReportsView, ReportAgingView

urlpatterns = [
   path('', ReportsView.as_view(), name='reportsapp'),
   path('finance/aging/', ReportAgingView.as_view(), name='report_aging'),
]
