# app_info/urls.py

from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path('calendrier/', views.calendrier_reservations, name='calendrier_reservations'),
    path('reserver/', views.ajouter_reservation, name='ajouter_reservation'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inscription/', SignUpView.as_view(), name='signup'),
    # ... autres chemins de votre application ...
]