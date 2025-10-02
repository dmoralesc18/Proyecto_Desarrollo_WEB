"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('Apps.Clients.urls')),
    path('core/', include('Apps.Core.urls')),
    path('documents/', include('Apps.Documents.urls')),
    path('equipment/', include('Apps.Equipment.urls')),
    path('finance/', include('Apps.Finance.urls')),
    path('home/', include('Apps.Home.urls')),
    path('inventory/', include('Apps.Inventory.urls')),
    path('projects/', include('Apps.Projects.urls')),
    path('quality/', include('Apps.Quality.urls')),
    path('reports/', include('Apps.Reports.urls')),
    path('subcontractors/', include('Apps.Subcontractors.urls')),
]
