from django.urls import path
from .views import (
    SupportCreateView,
    SupportSuccessView,
    login_view,
    logout_view,
    profile_view,
    user_list_view,
    user_create_view,
    user_edit_view,
    user_delete_view,
)

app_name = 'core'

urlpatterns = [
    path('support/', SupportCreateView.as_view(), name='support'),
    path('support/success/', SupportSuccessView.as_view(), name='support_success'),
    # Auth
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    # User management (admin only)
    path('users/', user_list_view, name='users'),
    path('users/create/', user_create_view, name='user_create'),
    path('users/<int:pk>/edit/', user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', user_delete_view, name='user_delete'),
]
