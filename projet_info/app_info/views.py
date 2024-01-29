# views.py
from django.http import HttpResponse

def accueil(request):
    return HttpResponse("<h1>Bienvenue sur mon site</h1>")
