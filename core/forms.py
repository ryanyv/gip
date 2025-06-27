from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'appearance-none block w-full px-3 py-2 bg-[#1f1f1f] border border-gold rounded-md text-white focus:outline-none focus:ring-gold focus:border-gold sm:text-sm',
            'rows': 5
        })
    )
