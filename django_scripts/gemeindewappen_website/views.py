from django.shortcuts import render, get_object_or_404
from .models import Wappen, Landkreis

# Create your views here.

def wappen_list(request):
    wappen_list = Wappen.objects.all()  # Alle Wappen abrufen
    return render(request, 'wappen_list.html', {'wappen_list': wappen_list})

def landkreise_list(request):
    # Alle Landkreise abrufen, bei denen der Typ "landkreis" ist
    landkreise = Landkreis.objects.filter(type='landkreis')
    return render(request, 'gemeindewappen_website/landkreise_list.html', {'landkreise': landkreise})

def landkreis_detail(request, pk):
    # Detailansicht eines Landkreises basierend auf der ID (pk)
    landkreis = get_object_or_404(Landkreis, id=id)
    return render(request, 'gemeindewappen_website/landkreis_detail.html', {'landkreis': landkreis})