from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
import random

class Table(models.Model):
    nom = models.CharField(max_length=50)
    capacite = models.IntegerField()

    def __str__(self):
        return self.nom
    

class Reservation(models.Model):
    # Vos autres champs de réservation
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.table} - {self.date_heure.strftime('%Y-%m-%d %H:%M')}"

    def get_absolute_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()
        if self.date_heure < timezone.now():
            raise ValidationError('La date et l\'heure ne peuvent pas être dans le passé')

        # Check if a table is available for the given number of people
        available_tables = Table.objects.filter(capacite__gte=self.nombre_personnes, reservation__date_heure__lt=self.date_heure)
        if available_tables.exists():
            self.table = random.choice(available_tables)
        else:
            raise ValidationError('Désolé, aucune table n\'est disponible')
