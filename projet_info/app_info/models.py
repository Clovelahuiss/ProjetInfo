from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.db.models import Min
import random
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Table(models.Model):
    id=models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    capacite = models.IntegerField()

    def __str__(self):
        return self.nom
    

class Reservation(models.Model):
    # Vos autres champs de réservation
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def assign_table(self):
        # Trouver les tables qui peuvent accueillir le nombre de personnes et qui ne sont pas déjà réservées à cette date/heure
        available_tables = Table.objects.annotate(
            surplus_capacity=models.F('capacite') - self.nombre_personnes
        ).filter(
            capacite__gte=self.nombre_personnes,
            # Assurez-vous que cette table n'a pas de réservation qui se chevauche avec l'heure demandée
        ).exclude(
            reservation__date_heure__date=self.date_heure.date(),
            reservation__date_heure__lte=self.date_heure,
            reservation__date_heure__gte=self.date_heure
        ).order_by('surplus_capacity')

        if available_tables.exists():
            self.table = available_tables.first()
        else:
            raise ValidationError('Aucune table disponible pour le nombre de personnes spécifié.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Assurez-vous que la méthode clean est appelée avant de sauvegarder
        super(Reservation, self).save(*args, **kwargs)

    def clean(self):
        if self.date_heure < timezone.now():
            raise ValidationError('La date et l\'heure ne peuvent pas être dans le passé')

        # Cette logique pourrait être incluse dans assign_table si vous préférez
        if not self.table:
            self.assign_table()

    def __str__(self):
        return f"{self.nom} - {self.table} - {self.date_heure.strftime('%Y-%m-%d %H:%M')}"