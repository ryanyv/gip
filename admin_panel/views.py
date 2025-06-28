from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
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
    """Display a list of all properties for admins."""
    properties = Property.objects.all()
    return render(request, 'admin_panel/manage_properties.html', {
        'properties': properties,
    })


@login_required
@user_passes_test(is_admin_or_superadmin)
def edit_property(request, pk):
    """Edit an existing property."""
    prop = get_object_or_404(Property, pk=pk)
    show_responsible = (
        request.user.is_superuser
        or getattr(request.user, "is_superadmin", False)
        or request.user.has_perm("properties.assign_responsible")
    )
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=prop, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('manage_properties')
    else:
        form = PropertyForm(instance=prop, user=request.user)
    return render(request, 'admin_panel/edit_property.html', {
        'form': form,
        'property': prop,
        'show_responsible': show_responsible,
    })


@login_required
@user_passes_test(is_admin_or_superadmin)
def delete_property(request, pk):
    """Delete a property permanently."""
    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    messages.success(request, "Property deleted.")
    return redirect('manage_properties')


@login_required
@user_passes_test(is_admin_or_superadmin)
def toggle_archive_property(request, pk):
    """Toggle the archived state of a property."""
    prop = get_object_or_404(Property, pk=pk)
    prop.is_archived = not getattr(prop, 'is_archived', False)
    prop.save()
    messages.success(
        request,
        "Property archived." if prop.is_archived else "Property restored.",
    )
    return redirect('manage_properties')
