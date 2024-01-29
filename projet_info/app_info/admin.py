from django.contrib import admin

from app_info.models import Table

table = Table(nom="Table 1", capacite=4)
table.save()


# Register your models here.
