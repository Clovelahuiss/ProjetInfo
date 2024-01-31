from django import forms
from .models import Reservation
from django.forms.widgets import DateTimeInput, HiddenInput

class ReservationForm(forms.ModelForm):
    table = forms.IntegerField(widget=HiddenInput(), required=False)

    class Meta:
        model = Reservation
        fields = ['nom', 'date_heure', 'nombre_personnes', 'table']
        widgets = {
            'date_heure': DateTimeInput(attrs={'type': 'datetime-local'}),
        }