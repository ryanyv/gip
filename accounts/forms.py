from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    no_commercial_emails = forms.BooleanField(
        required=False,
        label="I don't want to receive commercial emails",
    )
    agree_tos = forms.BooleanField(
        required=True,
        label="I agree with terms of service",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "profile_photo",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    field_order = [
        "profile_photo",
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "password1",
        "password2",
        "no_commercial_emails",
        "agree_tos",
    ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.no_commercial_emails = self.cleaned_data.get("no_commercial_emails", False)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = (
            "appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border "
            "border-gold rounded-md placeholder-gray-400 text-white "
            "focus:outline-none focus:ring-gold focus:border-gold sm:text-sm"
        )
        for name, field in self.fields.items():
            if name == "profile_photo":
                field.widget.attrs["class"] = "hidden"
            else:
                field.widget.attrs.setdefault("class", css_class)

            if field.help_text:
                auto_id = self.auto_id % self.add_prefix(name)
                field.widget.attrs.setdefault("data-hover-help", f"{auto_id}_helptext")
                field.widget.attrs.setdefault("data-help-text", str(field.help_text))
                field.help_text = ""
