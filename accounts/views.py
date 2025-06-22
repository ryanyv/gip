from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def logout_view(request):
    """Log out the user and redirect to the previous or home page."""
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


@login_required
def profile_view(request):
    """Display the logged in user's profile."""
    return render(request, 'accounts/profile.html')

