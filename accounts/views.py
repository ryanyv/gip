from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def logout_view(request):
    """Log out the user and redirect to the previous or home page."""
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


class RegisterView(CreateView):
    """User registration view using a custom form with email and phone."""
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

