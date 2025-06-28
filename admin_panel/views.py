from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from accounts.models import User
from properties.models import Property, Booking
from properties.forms import PropertyForm

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
    """List properties with management actions."""
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/manage_properties.html', {'properties': properties})


@login_required
@user_passes_test(is_admin_or_superadmin)
def edit_property(request, pk):
    """Edit an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    show_responsible = (
        request.user.is_superuser
        or getattr(request.user, 'is_superadmin', False)
        or request.user.has_perm('properties.assign_responsible')
    )
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('admin_panel:manage_properties')
    else:
        form = PropertyForm(instance=property_obj, user=request.user)
    return render(
        request,
        'admin_panel/edit_property.html',
        {'form': form, 'show_responsible': show_responsible, 'property': property_obj}
    )


@login_required
@user_passes_test(is_admin_or_superadmin)
def delete_property(request, pk):
    """Delete a property and redirect back to the list."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted.')
    return redirect('admin_panel:manage_properties')
