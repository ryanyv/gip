from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_panel_dashboard'),
    path('bookings/', views.manage_bookings, name='admin_panel_bookings'),
    path('bookings/<int:pk>/', views.property_calendar, name='admin_panel_property_calendar'),
    path('properties/', views.manage_properties, name='admin_panel_manage_properties'),
    path('properties/<int:pk>/delete/', views.delete_property, name='admin_panel_delete_property'),
]