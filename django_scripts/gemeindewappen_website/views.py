from django.shortcuts import render
from .models import Wappen, Entity, Normdaten, Population

# Create your views here.

def entity_list(request):
    entities = Entity.objects.exclude(type="ehem_landkreis")
    return render(request, 'frontpage.html', {'entities': entities})

def entity_detail(request, wikidata_id):
    entity = Entity.objects.get(wikidata_id=wikidata_id)
    normdaten = Normdaten.objects.get(wikidata_id=wikidata_id)
    wappen = Wappen.objects.get(wikidata_id=wikidata_id)
    population = Population.objects.filter(wikidata_id=wikidata_id).order_by('year')

    context = {
        'entity': entity,
        'normdaten': normdaten,
        'wappen': wappen,
        'population': population
    }

    return render(request, 'landkreis_detail.html', context)

def maps(request):
    return render(request, 'map.html')

def about(request):
    return render(request, 'about.html')
