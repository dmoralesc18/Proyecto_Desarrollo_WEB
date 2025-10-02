from django.contrib import admin
from django.urls import path, include
from Apps.Reports import views
from .views import ReportsView

urlpatterns = [
   path('', ReportsView.as_view(), name='reportsapp'),
]