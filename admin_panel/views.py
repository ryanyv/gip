from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_admin_or_superadmin(user):
    return user.is_authenticated and (getattr(user, 'is_admin', False) or getattr(user, 'is_superadmin', False))

@login_required
@user_passes_test(is_admin_or_superadmin)
def dashboard(request):
    # You can add stats or context here
    return render(request, 'admin_panel/dashboard.html')