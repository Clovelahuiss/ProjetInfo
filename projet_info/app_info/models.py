from django.db import models

class Table(models.Model):
    nom = models.CharField(max_length=50)
    capacite = models.IntegerField()

    def __str__(self):
        return self.nom

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    nombre_personnes = models.IntegerField()

    def __str__(self):
        return f"{self.table} - {self.date_heure.strftime('%Y-%m-%d %H:%M')}"
