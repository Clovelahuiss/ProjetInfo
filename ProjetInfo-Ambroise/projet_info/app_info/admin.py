from django.contrib import admin
from .models import Table, Reservation

# Enregistrez vos modèles ici
admin.site.register(Table)
admin.site.register(Reservation)