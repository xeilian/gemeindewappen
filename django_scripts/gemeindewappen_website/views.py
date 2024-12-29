from django.shortcuts import render
from .models import Wappen

# Create your views here.

def wappen_list(request):
    wappen_list = Wappen.objects.all()  # Alle Wappen abrufen
    return render(request, 'wappen_list.html', {'wappen_list': wappen_list})
