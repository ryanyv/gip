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
    """List properties for managing bookings."""
    filter_type = request.GET.get("type", "short-term")
    qs = Property.objects.all()
    if filter_type in ["short-term", "long-term", "investment"]:
        qs = qs.filter(property_type=filter_type)
    properties = qs.order_by("-created_at")
    return render(
        request,
        "admin_panel/manage_bookings.html",
        {"properties": properties, "filter_type": filter_type},
    )


@login_required
@user_passes_test(is_admin_or_superadmin)
def property_bookings(request, pk):
    """Display and manage bookings for a specific property."""
    from django.shortcuts import get_object_or_404, redirect
    from datetime import datetime, timedelta
    import json
    from django.core.serializers.json import DjangoJSONEncoder

    prop = get_object_or_404(Property, pk=pk)

    # Existing booked ranges
    bookings = Booking.objects.filter(property=prop, status="booked")
    booked = [
        {
            "start": b.start_date.isoformat(),
            "end": (b.end_date + timedelta(days=1)).isoformat(),
        }
        for b in bookings
    ]

    error = None
    success = None

    if request.method == "POST":
        start_str = request.POST.get("start_date")
        end_str = request.POST.get("end_date")
        try:
            start_date = datetime.fromisoformat(start_str).date() if start_str else None
            end_date = datetime.fromisoformat(end_str).date() if end_str else None
        except Exception:
            start_date = end_date = None

        if not start_date or not end_date or start_date >= end_date:
            error = "Please select a valid range."
        else:
            overlap = Booking.objects.filter(
                property=prop,
                status="booked",
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).exists()
            if overlap:
                error = "Those dates are already booked."
            else:
                Booking.objects.create(
                    property=prop,
                    user=request.user,
                    start_date=start_date,
                    end_date=end_date,
                    status="booked",
                )
                success = "Dates blocked successfully."
                # Refresh booked ranges to include the new booking
                bookings = Booking.objects.filter(property=prop, status="booked")
                booked = [
                    {
                        "start": b.start_date.isoformat(),
                        "end": (b.end_date + timedelta(days=1)).isoformat(),
                    }
                    for b in bookings
                ]

    context = {
        "property": prop,
        "booked_dates_json": json.dumps(booked, cls=DjangoJSONEncoder),
        "error": error,
        "success": success,
    }
    return render(request, "admin_panel/property_calendar.html", context)
