from django.contrib import admin
from django.urls import path, include  # Assurez-vous que 'path' et 'include' sont bien importés
from django.views.generic import RedirectView  # Importation de RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_info/', include('app_info.urls')),
    path('', RedirectView.as_view(url='app_info/calendrier/', permanent=True)),  # Redirection de l'URL racine
]