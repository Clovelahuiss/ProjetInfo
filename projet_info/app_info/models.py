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

    def assign_table(self):
        # Trouver les tables qui peuvent accueillir le groupe et qui ne sont pas déjà réservées à l'heure demandée
        available_tables = Table.objects.filter(capacite__gte=self.nombre_personnes).exclude(
            reservation__date_heure=self.date_heure
        )
        if available_tables:
            self.table = available_tables.first()
            self.save()
        else:
            # Gérer le cas où aucune table n'est disponible
            # Par exemple, vous pouvez définir 'table' à None ou gérer cette situation d'une autre manière
            self.table = None