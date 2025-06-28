from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.files.base import ContentFile
from .models import Property, Facility, Photo, Video
from PIL import Image
import tempfile
import subprocess
from io import BytesIO
import os


def compress_image(file, max_size=1280, quality=75):
    try:
        image = Image.open(file)
        image.thumbnail((max_size, max_size))
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        return ContentFile(buffer.getvalue(), name=file.name)
    except Exception:
        file.seek(0)
        return ContentFile(file.read(), name=file.name)


def compress_video(file, property_slug, order):
    ext = os.path.splitext(file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as src:
        for chunk in file.chunks():
            src.write(chunk)
    src_path = src.name
    dest = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    dest_path = dest.name
    dest.close()
    cmd = [
        "ffmpeg",
        "-i",
        src_path,
        "-vf",
        "scale='min(1920,iw)':-2",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        dest_path,
        "-y",
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with open(dest_path, "rb") as f:
        data = f.read()
    os.remove(src_path)
    os.remove(dest_path)
    filename = f"{property_slug}-{order+1}.mp4"
    return ContentFile(data, name=filename)


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
        widget=MultiFileInput(
            attrs={
                "class": "block w-full text-sm text-gray-300 file:bg-gold file:text-[#232323] file:font-semibold file:px-4 file:py-2 file:rounded file:border-0 file:mr-2",
                "accept": "image/*,video/*",
            }
        ),
        help_text="Upload one or more photos or videos",
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
        files = self.cleaned_data.get("photos", [])
        if commit:
            slug = slugify(property_obj.name)
            photo_idx = 0
            video_idx = 0
            for file in files:
                if getattr(file, "content_type", "").startswith("image"):
                    compressed = compress_image(file)
                    filename = f"{slug}-{photo_idx+1}.jpg"
                    photo = Photo(property=property_obj, order=photo_idx)
                    photo.image.save(filename, compressed, save=True)
                    photo_idx += 1
                elif getattr(file, "content_type", "").startswith("video"):
                    compressed_video = compress_video(file, slug, video_idx)
                    Video.objects.create(property=property_obj, video=compressed_video, order=video_idx)
                    video_idx += 1
        return property_obj
