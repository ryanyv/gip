from django.shortcuts import render

from properties.models import Property

def home(request):
    featured_properties = Property.objects.filter(is_featured=True)[:3]
    if not featured_properties:
        featured_properties = Property.objects.order_by("-created_at")[:3]
    return render(request, "core/home.html", {"featured_properties": featured_properties})

def about(request):
    return render(request, "core/about.html")