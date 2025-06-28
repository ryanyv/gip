from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('properties/', views.manage_properties, name='manage_properties'),
    path('properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:pk>/delete/', views.delete_property, name='delete_property'),
]