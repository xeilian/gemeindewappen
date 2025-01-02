from django.shortcuts import render
from .models import Wappen, Landkreis

# Create your views here.

def wappen_list(request):
    wappen_list = Wappen.objects.all()  
    return render(request, 'wappen_list.html', {'wappen_list': wappen_list})

def landkreise_list(request):
    landkreise = Landkreis.objects.all() 
    return render(request, 'gemeindewappen_website/landkreise_list.html', {'landkreise': landkreise})

def landkreis_detail(request, wikidata_id):
    landkreis = Landkreis.objects.get(wikidata_id=wikidata_id)
    return render(request, 'gemeindewappen_website/landkreis_detail.html', {'landkreis': landkreis})

def maps(request):
    return render(request, 'gemeindewappen_website/map.html')

def test(request):
    landkreis = {
        "name": "Zollernalbkreis",
        "blasonierung": "Goldenes Schild mit schwarzem Balken",
        "postleitzahl": "72336",
        "district_key": "08417",
        "area": "918.37",
        "population": "186764",
        "population_data": {
            "years": [2010, 2015, 2020],
            "values": [180000, 185000, 186764]
        },
        "coordinates": "8.71914,48.29123",
        "gnd": "123456789",
        "geonames": "987654321",
        "wikidata_id": "Q123456",
        "osm_relation": "1234567",
    }
    return render(request, "gemeindewappen_website/test.html", {"landkreis": landkreis})