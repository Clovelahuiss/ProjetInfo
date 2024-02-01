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
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

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


def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.nom = request.user.get_full_name() or request.user.username
                reservation.user = request.user  # Assurez-vous que votre modèle Reservation a un champ user
                reservation.save()
                messages.success(request, 'Réservation réussie.')
                return redirect('accueil')  # Rediriger vers la page du calendrier
            except ValidationError as e:
                form.add_error(None, str(e))
        else:
            print(form.errors)  # Affiche les erreurs de validation du formulaire
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'is_map_page': request.path == '/app_info/map/'  # Ajouter un indicateur pour la page map
    }
    return render(request, 'app_info/ajouter_reservation.html', context)

def accueil(request):
    # Renvoie le rendu de votre template HTML pour la page d'accueil
    return render(request, 'app_info/accueil.html')

def menu(request):
    # Renvoie le rendu de votre template HTML pour la page d'accueil
    return render(request, 'app_info/menu.html')