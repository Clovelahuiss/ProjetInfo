from django.db import models

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=100)
    # d'autres champs si nécessaire

    def __str__(self):
        return self.titre
