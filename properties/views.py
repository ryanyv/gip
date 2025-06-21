from django.shortcuts import render, get_object_or_404
from .models import Property
import json
from datetime import timedelta
from .models import Booking
from django.core.serializers.json import DjangoJSONEncoder

def property_list(request):
    filter_type = request.GET.get('type')
    qs = Property.objects.all()
    if filter_type in ['short-term', 'long-term', 'investment']:
        qs = qs.filter(property_type=filter_type)
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