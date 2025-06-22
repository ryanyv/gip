from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_photo",
            "role",
            "position",
            "phone_number",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = (
            "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border "
            "border-gold rounded-md placeholder-gray-400 text-white "
            "focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", css_class)
