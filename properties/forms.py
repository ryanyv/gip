from django import forms
from .models import Property, Facility, Photo


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PropertyForm(forms.ModelForm):
    photos = forms.FileField(
        required=False,
        widget=MultiFileInput(attrs={"class": "block w-full text-sm text-gray-300 file:bg-gold file:text-[#232323] file:font-semibold file:px-4 file:py-2 file:rounded file:border-0 file:mr-2"}),
        help_text="Upload one or more photos",
    )

    class Meta:
        model = Property
        fields = [
            "name",
            "property_type",
            "location",
            "description",
            "address",
            "guests",
            "bedrooms",
            "bathrooms",
            "area",
            "price_per_night",
            "latitude",
            "longitude",
            "facilities",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "property_type": forms.Select(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "location": forms.TextInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "description": forms.Textarea(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm",
                "rows": 4,
            }),
            "address": forms.TextInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "guests": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "bedrooms": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "bathrooms": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "area": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "price_per_night": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "latitude": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "longitude": forms.NumberInput(attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }),
            "facilities": forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2"
            }),
        }

    def save(self, commit=True):
        property_obj = super().save(commit)
        if commit and self.files.getlist("photos"):
            for order, image in enumerate(self.files.getlist("photos")):
                Photo.objects.create(property=property_obj, image=image, order=order)
        return property_obj
