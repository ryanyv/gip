from django import forms
from django.contrib.auth import get_user_model
from django.core.files import File
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
import os
import subprocess
import tempfile
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
        slug = slugify(property_obj.name or str(property_obj.pk))

        if commit:
            for order, image_file in enumerate(photos):
                img = Image.open(image_file)
                img.thumbnail((1280, 1280))
                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=80)
                buffer.seek(0)
                filename = f"{slug}-{order+1}.jpg"
                django_file = File(buffer, name=filename)
                Photo.objects.create(property=property_obj, image=django_file, order=order)

            for order, video_file in enumerate(videos):
                orig_ext = os.path.splitext(video_file.name)[1] or ".mp4"
                temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=orig_ext)
                for chunk in video_file.chunks():
                    temp_in.write(chunk)
                temp_in.flush()
                temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                temp_out.close()
                cmd = [
                    "ffmpeg",
                    "-i",
                    temp_in.name,
                    "-vf",
                    "scale='min(1920,iw)':min(1080,ih)",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "fast",
                    "-crf",
                    "23",
                    "-c:a",
                    "aac",
                    temp_out.name,
                ]
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    with open(temp_out.name, "rb") as f:
                        django_file = File(f, name=f"{slug}-video-{order+1}.mp4")
                        Video.objects.create(property=property_obj, file=django_file, order=order)
                finally:
                    os.remove(temp_in.name)
                    os.remove(temp_out.name)
        return property_obj
