from django.shortcuts import render
from .models import Reservation
from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
from django.db.models import Count, Sum
from django.http import HttpResponse

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')  # Rediriger vers la page de connexion après l'inscription
    template_name = 'app_info/signup.html'


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'app_info/Login.html'
    redirect_authenticated_user = False  # Rediriger les utilisateurs déjà connectés

    def get_success_url(self):
        return self.request.GET.get('next', '/')  # Rediriger vers la page d'accueil par défaut après la connexion

def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendrier_reservations')
    else:
        form = ReservationForm()
    return render(request, 'app_info/ajouter_reservation.html', {'form': form})

def historique(request):
    reservations = Reservation.objects.all()
    data = get_reservation_data()

    # Créer une structure de données pour les réservations et autres données
    result = {
        'reservations': reservations,
        'data': data
    }

    # Rendre le modèle avec les données directement dans le contexte
    return render(request, 'app_info/historique.html', result)

def calendrier_reservations(request):
    data = get_reservation_data()
    return render(request, 'app_info/calendrier.html', data)

def get_reservation_data():
    # Récupérer le nombre clients total
    clients = (
        Reservation.objects
        .values('date_heure__date')
        .annotate(nb_clients=Sum('nombre_personnes'))
    )
    
    # Récupérer le nombre clients par service du midi
    clients_midi = (
        Reservation.objects
        .filter(date_heure__hour__range=(11, 14))
        .values('date_heure__date')
        .annotate(nb_clients_midi=Sum('nombre_personnes'))
    )
    
    # Récupérer le nombre clients par service du soir
    clients_soir = (
        Reservation.objects
        .filter(date_heure__hour__range=(18, 21))
        .values('date_heure__date')
        .annotate(nb_clients_soir=Sum('nombre_personnes'))
    )

    # Récupérer le nombre de réservations par jour total
    reservations_par_jour = (
        Reservation.objects
        .values('date_heure__date')
        .annotate(nb_reservations_jour=Count('id'))
    )
    
    # Récupérer le nombre de réservations par jour et par service du midi
    reservations_midi = (
        Reservation.objects
        .filter(date_heure__hour__range=(11, 14))
        .values('date_heure__date')
        .annotate(nb_reservations_midi=Count('id'))
    )

    # Récupérer le nombre de réservations par jour et par service du soir
    reservations_soir = (
        Reservation.objects
        .filter(date_heure__hour__range=(18, 21))
        .values('date_heure__date')
        .annotate(nb_reservations_soir=Count('id'))
    )


    data_clients = [{
            'date': reservation['date_heure__date'],
            'nb_clients': reservation['nb_clients'],}
        for reservation in clients
    ]
    data_clients_midi = [{
            'date': reservation['date_heure__date'],
            'nb_clients_midi': reservation['nb_clients_midi'],}
        for reservation in clients_midi
    ]
    data_clients_soir = [{
            'date': reservation['date_heure__date'],
            'nb_clients_soir': reservation['nb_clients_soir'],}
        for reservation in clients_soir
    ]
    data_reservations_jour = [{
            'date': reservation['date_heure__date'],
            'nb_reservations_jour': reservation['nb_reservations_jour'],}
        for reservation in reservations_par_jour
    ]
    data_reservations_midi = [{
            'date': reservation['date_heure__date'],
            'nb_reservations_midi': reservation['nb_reservations_midi'],}
        for reservation in reservations_midi
    ]
    data_reservations_soir = [{
            'date': reservation['date_heure__date'],
            'nb_reservations_soir': reservation['nb_reservations_soir'],}
        for reservation in reservations_soir
    ]
   
    # Retourner les données au format JSON
    return {
        'nb_clients': data_clients,
        'nb_clients_midi': data_clients_midi,
        'nb_clients_soir': data_clients_soir,
        'nb_reservations_jour': data_reservations_jour,
        'nb_reservations_midi': data_reservations_midi,
        'nb_reservations_soir': data_reservations_soir,
    }
