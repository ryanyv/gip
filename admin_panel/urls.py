from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('properties/', views.manage_properties, name='admin_panel_manage_properties'),
    path('properties/delete/<int:pk>/', views.delete_property, name='admin_panel_delete_property'),
]