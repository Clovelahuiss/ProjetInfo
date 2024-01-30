from django.shortcuts import render
from .models import Reservation, Table
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages


def calendrier_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_info/calendrier.html', {'reservations': reservations})

def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendrier_reservations')  # Rediriger vers la page du calendrier
        else:
            print(form.errors)  # Affiche les erreurs de validation du formulaire
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'is_map_page': request.path == '/app_info/map/'  # Ajouter un indicateur pour la page map
    }
    return render(request, 'app_info/ajouter_reservation.html', context)

def map(request):
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Votre réservation a été effectuée avec succès.')
            return redirect('map')  # Redirigez vers la même page ou une autre selon vos besoins
    return render(request, 'app_info/map.html', {'form': form})

