from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.db.models import Min
import random
from django.contrib.auth.models import User
import datetime
from django.db.models import F
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def assign_table(self):
        # Trouver les tables qui peuvent accueillir le nombre de personnes et qui ne sont pas déjà réservées à cette date/heure
        available_tables = Table.objects.annotate(
            surplus_capacity=F('capacite') - self.nombre_personnes
        ).filter(
            capacite__gte=self.nombre_personnes,
            # Assurez-vous que cette table n'a pas de réservation qui se chevauche avec l'heure demandée
        ).exclude(
            reservation__date_heure__range=(self.date_heure, self.date_heure + datetime.timedelta(hours=1))
        ).order_by('surplus_capacity')

        print('Available tables:', available_tables)

        if available_tables.exists():
            self.table = available_tables.first()
            print('Assigned table:', self.table)
        else:
            raise ValidationError('Aucune table disponible pour le nombre de personnes spécifié.')

    def save(self, *args, **kwargs):
        self.assign_table()
        super(Reservation, self).save(*args, **kwargs)
        
    def clean(self):
        super().clean()

        if self.date_heure:
            date = self.date_heure.date()
            heure = self.date_heure.time()
            if self.date_heure.date() < timezone.now().date():
                raise ValidationError('La date de réservation est déjà passée.')

            heure_debut = datetime.time(heure.hour, heure.minute)
            datetime_obj = datetime.datetime.combine(date, heure_debut)
            self.date_heure = datetime_obj
            print('date_heure:', datetime_obj)
        
        else:
            print('date_heure is missing')
            return

        

    def __str__(self):
        return f"{self.nom} - {self.date_heure}-{self.table}"