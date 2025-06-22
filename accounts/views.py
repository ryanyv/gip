from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm


def logout_view(request):
    """Log out the user and redirect to the previous or home page."""
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


@login_required
def profile_view(request):
    """Display the logged in user's profile."""
    return render(request, 'accounts/profile.html')


def register_view(request):
    """Handle user registration and log the user in when successful."""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

