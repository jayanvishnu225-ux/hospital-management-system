
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import booking, contact



class bookingform(forms.ModelForm):

    class Meta:
        model = booking

        fields = [
            'patient_name',
            'patient_email',
            'patient_phone',
            'booking_on',
            'doctor'
        ]

        labels = {
            'patient_name': 'Patient Name',
            'patient_email': 'Patient Email',
            'patient_phone': 'Patient Phone',
            'booking_on': 'Booking Date',
            'doctor': 'Doctor'
        }

        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                
            }),

            'patient_email': forms.EmailInput(attrs={
                'class': 'form-control',
              
            }),

            'patient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),

            'booking_on': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'doctor': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['patient_name'].initial = user.username
            self.fields['patient_email'].initial = user.email


# Contact Form
class contactform(forms.ModelForm):

    class Meta:
        model = contact

        fields = ['name', 'email', 'phone', 'Address']

        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'Address': 'Address'
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),

            'Address': forms.Textarea(attrs={
                'placeholder': 'Enter your address',
                'class': 'form-control'
            })
        }


# Custom Signup Form
class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
