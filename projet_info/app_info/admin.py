from django.contrib import admin
from .models import Table, Reservation


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'capacite')  # Ajoutez les champs que vous voulez afficher

admin.site.register(Table, TableAdmin)
admin.site.register(Reservation)



