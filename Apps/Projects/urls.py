from django.urls import path
from .views import (
    ProjectsView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    BudgetCreateView,
    BudgetDetailView,
    BudgetUpdateView,
    BudgetDeleteView
)

urlpatterns = [
    # Projects URLs
    path('', ProjectsView.as_view(), name='projectsapp'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    
    # Budgets URLs
    path('budget/create/', BudgetCreateView.as_view(), name='budget_create'),
    path('budget/<int:pk>/', BudgetDetailView.as_view(), name='budget_detail'),
    path('budget/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget_update'),
    path('budget/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
]