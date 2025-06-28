from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('admin/', views.admin_property_list, name='admin_property_list'),
    path('<int:pk>/archive/', views.archive_property, name='archive_property'),
    path('<int:pk>/unarchive/', views.unarchive_property, name='unarchive_property'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
]