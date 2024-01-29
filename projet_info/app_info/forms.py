from django import forms
from .models import Reservation
from django.forms.widgets import DateTimeInput

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date_heure', 'nombre_personnes']
        widgets = {
            'date_heure': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
