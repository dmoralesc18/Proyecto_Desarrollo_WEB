from django.urls import path
from .views import SupportCreateView, SupportSuccessView

app_name = 'core'

urlpatterns = [
    path('support/', SupportCreateView.as_view(), name='support'),
    path('support/success/', SupportSuccessView.as_view(), name='support_success'),
]