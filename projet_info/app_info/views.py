from django.shortcuts import render
from .models import Reservation, Table
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Table
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from .models import Table, Reservation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Reservation
from django.core.serializers import serialize
# Dans votre fichier views.py
from django.shortcuts import redirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    # Redirection vers la liste des réservations ou une autre page appropriée
    return redirect('list_reservations')  # Assurez-vous d'avoir défini l'URL 'list_reservations'


@login_required
def modify_reservation(request, reservation_id):
    # Annule la réservation existante
    if cancel_reservation(request, reservation_id):
        # Redirige vers le formulaire de réservation après l'annulation
        return redirect('ajouter_reservation')

    else:
        # Gérer l'échec de l'annulation si nécessaire
        pass


@login_required
def list_reservations(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'app_info/list_reservations.html', {'reservations': user_reservations})


def reservation_details(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    tables = Table.objects.all()
    return render(request, 'app_info/reservation_details.html', {'reservation': reservation, 'tables': tables})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('accueil')  # ou toute autre page de redirection
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'app_info/signup.html', {'form': form})

def calendrier_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_info/calendrier.html', {'reservations': reservations})


def list_tables(request):
    tables = Table.objects.all()  # Récupère toutes les tables
    return render(request, 'app_info/list_tables.html', {'tables': tables})




def calendrier_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_info/calendrier.html', {'reservations': reservations})


@login_required
def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            if reservation.assign_table():  # Assurez-vous que la table est assignée
                reservation.save()
                # Redirection seulement si la réservation est enregistrée avec succès
                return redirect(reverse('reservation_details', kwargs={'reservation_id': reservation.id}))
            else:
                # Gère le cas où aucune table n'est disponible
                messages.error(request, "Aucune table disponible pour le nombre de personnes spécifié. Veuillez sélectionner une autre date ou modifier le nombre de personnes.")
        # Si le formulaire n'est pas valide ou aucune table n'est disponible
        return render(request, 'app_info/ajouter_reservation.html', {'form': form})
    else:
        form = ReservationForm()
        return render(request, 'app_info/ajouter_reservation.html', {'form': form})

def accueil(request):
    # Renvoie le rendu de votre template HTML pour la page d'accueil
    return render(request, 'app_info/accueil.html')

def menu(request):
    # Renvoie le rendu de votre template HTML pour la page d'accueil
    return render(request, 'app_info/menu.html')