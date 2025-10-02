from django.contrib import admin
from django.urls import path, include
from Apps.Projects import views
from .views import ProjectsView

urlpatterns = [
    path('', ProjectsView.as_view(), name='projectsapp'),
]
