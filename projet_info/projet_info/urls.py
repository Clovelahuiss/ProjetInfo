from django.contrib import admin
from django.urls import path, include  # Assurez-vous que 'path' et 'include' sont bien importés
from django.views.generic import RedirectView  # Importation de RedirectView
from app_info import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('app_info/', include('app_info.urls')),
   
]