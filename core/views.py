from django.shortcuts import render

from properties.models import Property
from accounts.models import User

def home(request):
    featured_properties = Property.objects.filter(is_featured=True)[:3]
    if not featured_properties:
        featured_properties = Property.objects.order_by("-created_at")[:3]
    return render(request, "core/home.html", {"featured_properties": featured_properties})

def about(request):
    team_members = User.objects.filter(is_team_member=True)
    return render(request, "core/about.html", {"team_members": team_members})

def contact(request):
    return render(request, "core/contact.html")

def privacy(request):
    return render(request, "core/privacy.html")
