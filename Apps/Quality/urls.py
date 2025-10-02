from django.contrib import admin
from django.urls import path, include
from Apps.Quality import views
from .views import QualityView

urlpatterns = [
   path('', QualityView.as_view(), name='qualityapp'),
]