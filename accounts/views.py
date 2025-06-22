from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def logout_view(request):
    """Log out the user and redirect to the previous or home page."""
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


class RegisterView(CreateView):
    """Simple user registration view using Django's built-in form."""
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

