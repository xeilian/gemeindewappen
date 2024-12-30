from django.shortcuts import render, get_object_or_404
from .models import Wappen, Landkreis

# Create your views here.

def wappen_list(request):
    wappen_list = Wappen.objects.all()  # Alle Wappen abrufen
    return render(request, 'wappen_list.html', {'wappen_list': wappen_list})

def landkreise_list(request):
    landkreise = Landkreis.objects.all()  # Ensure this fetches all valid Landkreise
    return render(request, 'gemeindewappen_website/landkreise_list.html', {'landkreise': landkreise})

def landkreis_detail(request, wikidata_id):
    landkreis = Landkreis.objects.get(wikidata_id=wikidata_id)
    return render(request, 'gemeindewappen_website/landkreis_detail.html', {'landkreis': landkreis})