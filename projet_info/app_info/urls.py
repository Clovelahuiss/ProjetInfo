# app_info/urls.py

from django.urls import path, include
from . import views
from .views import login_view

urlpatterns = [
    path('calendrier/', views.calendrier_reservations, name='calendrier_reservations'),
    path('reserver/', views.ajouter_reservation, name='ajouter_reservation'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accueil/', views.accueil, name='accueil'),
    path('accounts/login/', views.login_view, name='login'),
    path('menu/', views.menu, name='menu'),
     path('signup/', views.signup_view, name='signup'),
]
