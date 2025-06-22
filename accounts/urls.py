from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', lambda request: HttpResponse("Profile page"), name='profile'),
]
