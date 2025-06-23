from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'profile_photo',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'}),
            'username': forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'}),
            'phone_number': forms.TextInput(attrs={'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'}),
            'profile_photo': forms.FileInput(attrs={'class': 'hidden', 'accept': 'image/*'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'
            }),
        }
