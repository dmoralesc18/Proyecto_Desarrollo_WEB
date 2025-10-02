from django.contrib import admin
from django.urls import path, include
from Apps.Finance import views
from .views import FinanceView

urlpatterns = [
   path('', FinanceView.as_view(), name='financeapp'),
]