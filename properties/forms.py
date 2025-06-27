from django import forms
from django.contrib.auth import get_user_model
from .models import Property, Facility, Photo
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import os
import tempfile
from moviepy import VideoFileClip


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
    video = forms.FileField(required=False)
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
            "video",
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
        video = self.cleaned_data.get("video")

        if commit:
            slug = slugify(property_obj.name) or f"property_{property_obj.pk}"

            if video:
                processed_video = self._process_video(video, slug)
                property_obj.video = processed_video
                property_obj.save(update_fields=["video"])

            for order, image in enumerate(photos, start=1):
                processed_image = self._process_image(image, slug, order)
                Photo.objects.create(property=property_obj, image=processed_image, order=order)

        return property_obj

    def _process_image(self, uploaded_file, slug, index):
        try:
            uploaded_file.seek(0)
            img = Image.open(uploaded_file)
            img.thumbnail((1600, 1600))
            buffer = BytesIO()
            format_ = img.format or "JPEG"
            img.save(buffer, format=format_, optimize=True, quality=75)
            buffer.seek(0)
            ext = "jpg" if format_.lower() == "jpeg" else format_.lower()
            file_name = f"{slug}_{index}.{ext}"
            return InMemoryUploadedFile(buffer, None, file_name, f"image/{ext}", buffer.getbuffer().nbytes, None)
        except Exception:
            uploaded_file.seek(0)
            ext = os.path.splitext(uploaded_file.name)[1]
            uploaded_file.name = f"{slug}_{index}{ext}"
            return uploaded_file

    def _process_video(self, uploaded_file, slug):
        try:
            ext = os.path.splitext(uploaded_file.name)[1] or ".mp4"
            temp_in = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            for chunk in uploaded_file.chunks():
                temp_in.write(chunk)
            temp_in.flush()

            clip = VideoFileClip(temp_in.name)
            if clip.h > 1080:
                clip = clip.resize(height=1080)
            temp_out = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            clip.write_videofile(temp_out.name, codec="libx264", audio_codec="aac", logger=None)
            clip.close()
            temp_in.close()

            processed_file = open(temp_out.name, "rb")
            new_file = InMemoryUploadedFile(processed_file, None, f"{slug}{ext}", "video/mp4", os.path.getsize(temp_out.name), None)
            return new_file
        except Exception:
            uploaded_file.seek(0)
            uploaded_file.name = f"{slug}{os.path.splitext(uploaded_file.name)[1]}"
            return uploaded_file
