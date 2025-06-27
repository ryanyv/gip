from django.shortcuts import render
from .forms import ContactForm

def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

def contact(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real project you might send an email here
            success = True
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form, "success": success})
