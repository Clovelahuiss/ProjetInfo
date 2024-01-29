from django.shortcuts import render
from .models import Reservation
from django.shortcuts import render, redirect
from .forms import ReservationForm

def calendrier_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'app_info/calendrier.html', {'reservations': reservations})

def ajouter_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendrier_reservations')
    else:
        form = ReservationForm()
    return render(request, 'app_info/ajouter_reservation.html', {'form': form})