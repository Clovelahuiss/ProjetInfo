from django import forms
from .models import Reservation
from django.forms.widgets import DateTimeInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ReservationForm(forms.ModelForm):
    table = forms.IntegerField(widget=HiddenInput(), required=False)

    class Meta:
        model = Reservation
        fields = ['nom', 'date_heure', 'nombre_personnes', 'table']
        widgets = {
            'date_heure': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.')
    phone = forms.CharField(max_length=20, help_text='Requis. Entrez un numéro de téléphone.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )