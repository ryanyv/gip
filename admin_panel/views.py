from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
import json
from django.core.serializers.json import DjangoJSONEncoder
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
    """Display a calendar for a property and allow blocking dates."""
    property_obj = get_object_or_404(Property, pk=pk)

    bookings = Booking.objects.filter(property=property_obj, status="booked")
    from datetime import timedelta, datetime
    booked_dates = [
        {
            "start": b.start_date.isoformat(),
            "end": (b.end_date + timedelta(days=1)).isoformat(),
            "title": "Booked",
        }
        for b in bookings
    ]

    error = success = None
    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        try:
            start_date = datetime.fromisoformat(start_date_str).date()
            end_date = datetime.fromisoformat(end_date_str).date()
        except Exception:
            start_date = end_date = None
        if not start_date or not end_date or start_date >= end_date:
            error = "Please select a valid date range."
        else:
            overlap = Booking.objects.filter(
                property=property_obj,
                status="booked",
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).exists()
            if overlap:
                error = "Dates overlap with an existing booking."
            else:
                Booking.objects.create(
                    property=property_obj,
                    user=request.user,
                    start_date=start_date,
                    end_date=end_date,
                    status="booked",
                )
                success = "Dates blocked successfully."
                bookings = Booking.objects.filter(property=property_obj, status="booked")
                booked_dates = [
                    {
                        "start": b.start_date.isoformat(),
                        "end": (b.end_date + timedelta(days=1)).isoformat(),
                        "title": "Booked",
                    }
                    for b in bookings
                ]

    context = {
        "property": property_obj,
        "booked_dates_json": json.dumps(booked_dates, cls=DjangoJSONEncoder),
        "error": error,
        "success": success,
    }
    return render(request, "admin_panel/property_bookings.html", context)
