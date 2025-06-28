from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('properties/', views.property_management, name='admin_panel_property_management'),
]