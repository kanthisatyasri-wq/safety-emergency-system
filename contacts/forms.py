from django import forms
from .models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):

    class Meta:

        model = EmergencyContact

        fields = [
            'contact_type',
            'name',
            'email',
            'phone',
        ]

        widgets = {

            'contact_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter contact name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number',
                    'maxlength': '15'
                }
            ),
        }
