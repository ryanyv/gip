from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', lambda request: HttpResponse("Profile page"), name='profile'),
]
