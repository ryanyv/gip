from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from admin_panel.views import is_admin_or_superadmin
from .models import Property, Booking
from django.db.models import Q
from datetime import datetime
import json
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
from .forms import PropertyForm

def property_list(request):
    filter_type = request.GET.get('type')
    qs = Property.objects.all()
    if filter_type in ['short-term', 'long-term', 'investment']:
        qs = qs.filter(property_type=filter_type)

    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(location__icontains=q) | Q(address__icontains=q))

    guests = request.GET.get('guests')
    try:
        if guests:
            guests_int = int(guests)
            qs = qs.filter(guests__gte=guests_int)
    except (TypeError, ValueError):
        pass

    checkin  = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    start = end = None
    try:
        if checkin and checkout:
            start = datetime.fromisoformat(checkin).date()
            end   = datetime.fromisoformat(checkout).date()
    except Exception:
        start = end = None
    if start and end and start < end:
        qs = qs.exclude(
            bookings__status='booked',
            bookings__start_date__lt=end,
            bookings__end_date__gt=start,
        )

    properties = qs.order_by('-created_at')
    # Ranges for filter dropdowns
    guest_range = range(1, 13)     # 1‑12 guests
    bedroom_range = range(1, 9)    # 1‑8 bedrooms
    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'filter_type': filter_type,
        'guest_range': guest_range,
        'bedroom_range': bedroom_range,
    })

def property_detail(request, pk):
    from django.core.mail import send_mail  # Optional: if you want to send emails
    from django.utils import timezone

    property = get_object_or_404(Property, pk=pk)
    # Get all bookings with status 'booked'
    bookings = Booking.objects.filter(property=property, status='booked')
    booked_dates = [
        {
            'start': booking.start_date.isoformat(),
            'end': (booking.end_date + timedelta(days=1)).isoformat(),  # FullCalendar's end is exclusive
            'title': 'Booked'
        }
        for booking in bookings
    ]

    reservation_error = None
    reservation_success = None

    # Reservation logic (POST)
    if request.method == "POST":
        start_date_str = request.POST.get('start_date')
        end_date_str   = request.POST.get('end_date')
        guest_name     = request.POST.get('guest_name')
        guest_email    = request.POST.get('guest_email')
        user = request.user if request.user.is_authenticated else None

        from datetime import datetime
        try:
            start_date = datetime.fromisoformat(start_date_str).date() if start_date_str else None
            end_date   = datetime.fromisoformat(end_date_str).date() if end_date_str else None
        except Exception:
            start_date = end_date = None

        # Validate input
        if not start_date or not end_date or start_date >= end_date:
            reservation_error = "Please select a valid date range."
        else:
            # Check for overlap with any booked range
            overlap = Booking.objects.filter(
                property=property,
                status='booked',
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            if overlap:
                reservation_error = "Those dates are already booked."
            else:
                booking = Booking.objects.create(
                    property=property,
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    guest_name=guest_name if not user else user.get_full_name(),
                    guest_email=guest_email if not user else user.email,
                    status='booked'
                )
                reservation_success = "Reservation successful! We will contact you soon."
                # Optionally, send email to admin/guest here

    return render(request, 'properties/property_detail.html', {
        'property': property,
        'booked_dates_json': json.dumps(booked_dates, cls=DjangoJSONEncoder),
        'reservation_error': reservation_error,
        'reservation_success': reservation_success,
    })

@login_required
@user_passes_test(is_admin_or_superadmin)
def add_property(request):
    show_responsible = (
        request.user.is_superuser
        or getattr(request.user, "is_superadmin", False)
        or request.user.has_perm("properties.assign_responsible")
    )
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            prop = form.save()
            if not prop.responsible:
                prop.responsible = request.user
                prop.save()
            messages.success(request, "Property added successfully.")
            return redirect('properties:property_list')
    else:
        form = PropertyForm(initial={"responsible": request.user.pk}, user=request.user)
    return render(request, 'properties/add_property.html', {'form': form, 'show_responsible': show_responsible})
