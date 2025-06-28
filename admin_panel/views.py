from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from properties.forms import PropertyForm
from accounts.models import User
from properties.models import Property, Booking

def is_admin_or_superadmin(user):
    """Return True if the user has admin privileges."""
    return user.is_authenticated and (
        getattr(user, 'is_admin', False)
        or getattr(user, 'is_superadmin', False)
        or user.is_superuser
    )

@login_required
@user_passes_test(is_admin_or_superadmin)
def dashboard(request):
    """Render the management dashboard with some basic statistics."""
    context = {
        'properties_count': Property.objects.count(),
        'bookings_count': Booking.objects.count(),
    }
    if request.user.is_superadmin or request.user.is_superuser:
        context['users_count'] = User.objects.count()
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
@user_passes_test(is_admin_or_superadmin)
def manage_properties(request):
    """Display all properties for management."""
    properties = Property.objects.all().select_related('responsible')
    return render(request, 'admin_panel/manage_properties.html', {'properties': properties})


@login_required
@user_passes_test(is_admin_or_superadmin)
def edit_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    show_responsible = (
        request.user.is_superuser
        or getattr(request.user, 'is_superadmin', False)
        or request.user.has_perm('properties.assign_responsible')
    )
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('admin_panel:manage_properties')
    else:
        form = PropertyForm(instance=prop, user=request.user)
    return render(request, 'properties/add_property.html', {'form': form, 'show_responsible': show_responsible})


@login_required
@user_passes_test(is_admin_or_superadmin)
def toggle_archive_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.is_archived = not prop.is_archived
    prop.save()
    if prop.is_archived:
        messages.success(request, 'Property archived.')
    else:
        messages.success(request, 'Property restored.')
    return redirect('admin_panel:manage_properties')


@login_required
@user_passes_test(is_admin_or_superadmin)
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, 'Property deleted.')
    return redirect('admin_panel:manage_properties')
