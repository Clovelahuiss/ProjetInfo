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
from django.utils.timezone import make_aware, get_default_timezone



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
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def assign_table(self):
        available_tables = Table.objects.annotate(
            surplus_capacity=F('capacite') - self.nombre_personnes
        ).filter(
            capacite__gte=self.nombre_personnes,
        ).exclude(
            reservation__date_heure__range=(self.date_heure, self.date_heure + datetime.timedelta(hours=1))
        ).order_by('surplus_capacity')

        if available_tables.exists():
            self.table = available_tables.first()
            return True  # Indique que l'assignation a réussi
        else:
            return False  # Indique qu'aucune table n'est disponible

    def save(self, *args, **kwargs):
        self.assign_table()
        super(Reservation, self).save(*args, **kwargs)
        
    def clean(self):
        super().clean()

        if self.date_heure:
            date = self.date_heure.date()
            heure = self.date_heure.time()
            if timezone.is_naive(self.date_heure):
                self.date_heure = make_aware(self.date_heure, get_default_timezone())
            if self.date_heure < timezone.now():
                raise ValidationError('La date de réservation est déjà passée.')

            heure_debut = datetime.time(heure.hour, heure.minute)
            datetime_obj = datetime.datetime.combine(date, heure_debut)
            self.date_heure = datetime_obj
            print('date_heure:', datetime_obj)
        
        else:
            print('date_heure is missing')
            return

        

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.date_heure} - Table: {self.table.nom if self.table else 'Pas de table assignée'}"
        else:
            return f"Utilisateur inconnu - {self.date_heure} - Table: {self.table.nom if self.table else 'Pas de table assignée'}"