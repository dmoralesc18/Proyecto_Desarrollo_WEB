from django.contrib import admin
from django.urls import path, include
from Apps.Subcontractors import views
from .views import SubcontractorsView

urlpatterns = [
   path('', SubcontractorsView.as_view(), name='subcontractorsapp')
]