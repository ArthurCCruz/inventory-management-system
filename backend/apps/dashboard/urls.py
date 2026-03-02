from .views import DashboardView
from django.urls import path

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]