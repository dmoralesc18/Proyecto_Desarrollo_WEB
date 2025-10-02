from django.contrib import admin
from django.urls import path, include
from Apps.Documents import views
from .views import DocumentsView

urlpatterns = [
   path('documents/', DocumentsView.as_view(), name='documentsapp'),
]