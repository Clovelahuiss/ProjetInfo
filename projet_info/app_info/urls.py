# app_info/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calendrier/', views.calendrier_reservations, name='calendrier_reservations'),
    path('reserver/', views.ajouter_reservation, name='ajouter_reservation'),
    # ... autres chemins de votre application ...
]
