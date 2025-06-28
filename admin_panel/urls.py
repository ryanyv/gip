from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('properties/', views.manage_properties, name='admin_panel_manage_properties'),
]