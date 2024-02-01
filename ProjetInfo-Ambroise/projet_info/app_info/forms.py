from django import forms
from .models import Reservation
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Informez une adresse email valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class CustomAuthenticationForm(AuthenticationForm):
    # Ici vous pouvez personnaliser votre formulaire d'authentification
    pass


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_heure', 'nombre_personnes','nom']
        widgets = {
            'date_heure': DateTimeInput(attrs={'type': 'datetime-local'}),
        }