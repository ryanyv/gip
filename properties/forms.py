from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.base import ContentFile
import subprocess
import os
import tempfile
from io import BytesIO
from PIL import Image
from .models import Property, Facility, Photo, Video


class MultiFileInput(forms.ClearableFileInput):
    """File input that allows selecting multiple files."""

    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    """File field that returns a list of uploaded files."""

    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        return data

    def validate(self, data):
        if self.required and not data:
            super().validate(None)

class PropertyForm(forms.ModelForm):
    photos = MultiFileField(
        required=False,
        widget=MultiFileInput(attrs={"class": "block w-full text-sm text-gray-300 file:bg-gold file:text-[#232323] file:font-semibold file:px-4 file:py-2 file:rounded file:border-0 file:mr-2"}),
        help_text="Upload one or more photos",
    )
    videos = MultiFileField(
        required=False,
        widget=MultiFileInput(attrs={"class": "block w-full text-sm text-gray-300 file:bg-gold file:text-[#232323] file:font-semibold file:px-4 file:py-2 file:rounded file:border-0 file:mr-2"}),
        help_text="Upload one or more videos",
    )
    responsible = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
            }
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not (
            user.is_superuser
            or getattr(user, "is_superadmin", False)
            or user.has_perm("properties.assign_responsible")
        ):
            self.fields.pop("responsible")

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
            "responsible",
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
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "facilities": forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2"
            }),
        }

    def save(self, commit=True):
        property_obj = super().save(commit)
        photos = self.cleaned_data.get("photos", [])
        videos = self.cleaned_data.get("videos", [])

        if commit:
            for order, image in enumerate(photos):
                processed = self._process_image(image, property_obj.name, order)
                Photo.objects.create(property=property_obj, image=processed, order=order)

            for order, video in enumerate(videos):
                processed = self._process_video(video, property_obj.name, order)
                Video.objects.create(property=property_obj, video=processed, order=order)

        return property_obj

    def _process_image(self, uploaded_file, prop_name, order):
        try:
            img = Image.open(uploaded_file)
            img.thumbnail((1280, 1280))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            buffer = BytesIO()
            format = img.format if img.format else "JPEG"
            img.save(buffer, format=format, quality=75)
            buffer.seek(0)
            data = buffer.read()
        except Exception:
            uploaded_file.seek(0)
            data = uploaded_file.read()
        ext = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        new_name = f"{slugify(prop_name)}_{order + 1}{ext}"
        return ContentFile(data, name=new_name)

    def _process_video(self, uploaded_file, prop_name, order):
        ext = os.path.splitext(uploaded_file.name)[1] or ".mp4"
        new_name = f"{slugify(prop_name)}_{order + 1}{ext}"
        with tempfile.NamedTemporaryFile(suffix=ext) as src:
            for chunk in uploaded_file.chunks():
                src.write(chunk)
            src.flush()
            out = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
            out.close()
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                src.name,
                "-vf",
                "scale=1920:1080:force_original_aspect_ratio=decrease",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "28",
                out.name,
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                with open(out.name, "rb") as f:
                    data = f.read()
                os.remove(out.name)
            except Exception:
                uploaded_file.seek(0)
                data = uploaded_file.read()
        return ContentFile(data, name=new_name)
