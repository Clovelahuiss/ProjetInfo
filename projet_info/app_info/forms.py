from django import forms
from .models import Reservation
from django.forms.widgets import DateTimeInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.forms import Select


class ReservationForm(forms.ModelForm):
    # Ajout d'un champ de choix pour les créneaux horaires
    time_slot = forms.ChoiceField(choices=[
        ('12:00', '12-13h'),
        ('13:00', '13-14h'),
        ('19:00', '19-20h'),
        ('20:00', '20-21h'),
    ], label="Créneau horaire")

    class Meta:
        model = Reservation
        fields = ['nom', 'nombre_personnes']
        # Le champ 'date_heure' est géré manuellement, donc pas inclus dans 'fields'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialisation du champ 'date_heure' pour utiliser un widget de type 'date'
        self.fields['date_heure'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date")

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date_heure')
        time_slot = cleaned_data.get('time_slot')

        if date and time_slot:
            heure_debut = datetime.time(int(time_slot[:2]), int(time_slot[3:5]))
            datetime_obj = datetime.datetime.combine(date, heure_debut)
            cleaned_data['date_heure'] = datetime_obj

        return cleaned_data

    def save(self, commit=True):
        instance = super(ReservationForm, self).save(commit=False)
        instance.date_heure = self.cleaned_data.get('date_heure')
        instance.assign_table()

        if commit:
            instance.save()
        return instance
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requis. Entrez une adresse email valide.')
    phone = forms.CharField(max_length=20, help_text='Requis. Entrez un numéro de téléphone.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )