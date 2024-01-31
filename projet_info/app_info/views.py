from django.shortcuts import render
from .models import Reservation, Table
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Table
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

# ... autres imports ...

def map(request):
    form = ReservationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)

        # Récupérer l'ID de la table à partir du champ caché et convertir en entier si non vide
        table_id = request.POST.get('table')
        if table_id:
            try:
                table_id = int(table_id)  # Conversion de l'ID en entier
                table = get_object_or_404(Table, pk=table_id)  # Récupération de l'instance de Table
                reservation.table = table  # Assignation de l'instance à la réservation
            except ValueError:
                # Gestion de l'erreur si la conversion en entier échoue
                messages.error(request, "ID de table invalide.")
                return render(request, 'app_info/map.html', {'form': form})
        else:
            messages.error(request, "Aucune table sélectionnée.")
            return render(request, 'app_info/map.html', {'form': form})

        reservation.save()  # Sauvegarde de la réservation avec la table assignée
        messages.success(request, "Votre réservation a été enregistrée.")
        return redirect('map')

    return render(request, 'app_info/map.html', {'form': form})
