from django.shortcuts import render

from properties.models import Property
from accounts.models import User

def home(request):
    featured_properties = Property.objects.filter(is_featured=True, is_archived=False)[:3]
    if not featured_properties:
        featured_properties = Property.objects.filter(is_archived=False).order_by("-created_at")[:3]
    return render(request, "core/home.html", {"featured_properties": featured_properties})

def about(request):
    team_members = User.objects.filter(show_on_team_page=True)
    return render(request, "core/about.html", {"team_members": team_members})

def contact(request):
    return render(request, "core/contact.html")

def privacy(request):
    return render(request, "core/privacy.html")
