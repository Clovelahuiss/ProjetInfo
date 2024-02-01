# app_info/urls.py

from django.urls import path
from . import views
from .views import CustomLoginView
from .views import SignUpView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('calendrier/', views.calendrier_reservations, name='calendrier_reservations'),
    path('reserver/', views.ajouter_reservation, name='ajouter_reservation'),
    path('connexion/', CustomLoginView.as_view(), name='login'),
    path('inscription/', SignUpView.as_view(), name='signup'),
    path('historique/', views.historique, name='historique'),
]
