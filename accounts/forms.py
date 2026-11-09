from django import forms
from .models import User


class SignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password'
            }
        )
    )

    aadhaar_number = forms.CharField(
        max_length=12,
        min_length=12,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter 12-digit Aadhaar number',
                'maxlength': '12',
                'inputmode': 'numeric'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password',
            'aadhaar_number',
        ]