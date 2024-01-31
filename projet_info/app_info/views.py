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
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # Rediriger vers la page de connexion après l'inscription
    template_name = 'app_info/signup.html'

def calendrier_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_info/calendrier.html', {'reservations': reservations})

def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.nom = request.user.get_full_name() or request.user.username
            reservation.user = request.user  # Assurez-vous que votre modèle Reservation a un champ user
            reservation.save()
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
    reservation.user = request.user
    reservation.save()

# ... autres imports ...
