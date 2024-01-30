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
    nom = models.CharField(max_length=100)
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Vérifie si c'est une nouvelle instance
            # Ici, personnalisez la logique pour définir le nom de la réservation
            self.nom_reservation = self.nom 
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.table} - {self.date_heure.strftime('%Y-%m-%d %H:%M')}"

    def get_absolute_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()
        if self.date_heure and self.date_heure < timezone.now():
            raise ValidationError('La date et l\'heure ne peuvent pas être dans le passé')

            # Trouver les réservations qui se chevauchent avec la date et l'heure demandées
            overlapping_reservations = Reservation.objects.filter(
                tablecapacitegte=self.nombre_personnes,
                date_heure=self.date_heure
            )

            # S'il y a des réservations qui se chevauchent, la table n'est pas disponible
            if overlapping_reservations.exists():
                raise ValidationError('Désolé, aucune table n\'est disponible à cette date et heure')

            # Si aucune réservation ne se chevauche, trouver une table disponible
            available_tables = Table.objects.filter(capacitegte=self.nombre_personnes).exclude(
                reservationin=overlapping_reservations
            )

            # S'il y a des tables disponibles, affecter une à la réservation
            if available_tables.exists():
                self.table = available_tables.first()  # Affecter la première table disponible
            else:
                raise ValidationError('Désolé, aucune table n\'est disponible pour le nombre de personnes spécifié')