from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.urls import reverse 

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
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.table} - {self.date_heure.strftime('%Y-%m-%d %H:%M')}- {self.nom}"

    def get_absolute_url(self):
        return reverse('reservation-detail', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()
        if self.date_heure < timezone.now():
            raise ValidationError('La date et l\'heure ne peuvent pas être dans le passé')

         # Vérifier si l'heure de la réservation est en dehors des services du midi et du soir
        heure_reservation = self.date_heure.hour
        if not (11 <= heure_reservation <= 14 or 18 <= heure_reservation <= 22):
            raise ValidationError('Impossible de réserver en dehors des services du midi (9h-14h) et du soir (18h-22h)')

        # Trouver les réservations qui se chevauchent avec la date et l'heure demandées
        overlapping_reservations = Reservation.objects.filter(
            table__capacite__gte=self.nombre_personnes,
            date_heure=self.date_heure
        )

        # Trouver les réservations qui se chevauchent avec la date et l'heure demandées
        overlapping_reservations = Reservation.objects.filter(
            table__capacite__gte=self.nombre_personnes,
            date_heure=self.date_heure
        )

        # S'il y a des réservations qui se chevauchent, la table n'est pas disponible
        if overlapping_reservations.exists():
            raise ValidationError('Désolé, aucune table n\'est disponible à cette date et heure')

        # Si aucune réservation ne se chevauche, trouver une table disponible
        available_tables = Table.objects.filter(capacite__gte=self.nombre_personnes).exclude(
            reservation__in=overlapping_reservations
        )

        # S'il y a des tables disponibles, affecter une à la réservation
        if available_tables.exists():
            self.table = available_tables.first()  # Affecter la première table disponible
        else:
            raise ValidationError('Désolé, aucune table n\'est disponible pour le nombre de personnes spécifié')
