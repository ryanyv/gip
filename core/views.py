from django.shortcuts import render

from properties.models import Property
from .models import TeamMember

def home(request):
    featured_properties = Property.objects.filter(is_featured=True)[:3]
    if not featured_properties:
        featured_properties = Property.objects.order_by("-created_at")[:3]
    return render(request, "core/home.html", {"featured_properties": featured_properties})

def about(request):
    team = TeamMember.objects.select_related("user")
    return render(request, "core/about.html", {"team_members": team})

def contact(request):
    return render(request, "core/contact.html")

def privacy(request):
    return render(request, "core/privacy.html")
