from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
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
    """Custom property management page listing all properties."""
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/manage_properties.html', {
        'properties': properties,
    })


@login_required
@user_passes_test(is_admin_or_superadmin)
def delete_property(request, pk):
    """Delete a property via AJAX from the management page."""
    if request.method != "POST":
        from django.http import HttpResponseNotAllowed
        return HttpResponseNotAllowed(["POST"])

    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse

    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    return JsonResponse({"deleted": True})


@login_required
@user_passes_test(is_admin_or_superadmin)
def manage_bookings(request):
    """List bookings filtered by selected short-term property."""
    property_id = request.GET.get("property")
    properties = Property.objects.filter(property_type="short-term").order_by("name")
    selected_property = None
    bookings = Booking.objects.none()

    if property_id:
        selected_property = Property.objects.filter(id=property_id, property_type="short-term").first()
        if selected_property:
            bookings = Booking.objects.filter(property=selected_property).order_by("-start_date")

    context = {
        "properties": properties,
        "bookings": bookings,
        "selected_property": selected_property,
    }
    return render(request, "admin_panel/manage_bookings.html", context)
