from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('properties/', views.manage_properties, name='manage_properties'),
    path('properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:pk>/archive/', views.toggle_archive_property, name='toggle_archive_property'),
    path('properties/<int:pk>/delete/', views.delete_property, name='delete_property'),
]