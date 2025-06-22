from django.shortcuts import render, get_object_or_404
from .models import Property
from .models import Booking
import json
from datetime import timedelta, date
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

def property_list(request):
    filter_type = request.GET.get('type')
    q = request.GET.get('q')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')

    qs = Property.objects.all()

    if filter_type in ['short-term', 'long-term', 'investment']:
        qs = qs.filter(property_type=filter_type)

    if q:
        qs = qs.filter(Q(location__icontains=q) | Q(name__icontains=q))

    if guests:
        try:
            guest_count = int(guests)
            qs = qs.filter(guests__gte=guest_count)
        except ValueError:
            pass

    # Date range filtering - exclude properties with overlapping bookings
    if checkin and checkout:
        try:
            start = date.fromisoformat(checkin)
            end = date.fromisoformat(checkout)
            qs = qs.exclude(
                bookings__status='booked',
                bookings__start_date__lt=end,
                bookings__end_date__gt=start,
            )
        except ValueError:
            pass

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
    return render(request, 'properties/property_detail.html', {
        'property': property,
        'booked_dates_json': json.dumps(booked_dates, cls=DjangoJSONEncoder)
    })