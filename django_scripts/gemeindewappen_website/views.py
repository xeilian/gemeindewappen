from django.shortcuts import render
from django.db.models import Max
from .models import *

# Create your views here.

def entity_list(request):
    entities = Entity.objects.exclude(type="ehem_landkreis")
    return render(request, 'frontpage.html', {'entities': entities})

def entity_detail(request, wikidata_id):
    entity = Entity.objects.get(wikidata_id=wikidata_id)
    normdaten = Normdaten.objects.get(wikidata_id=wikidata_id)
    wappen = Wappen.objects.get(wikidata_id=wikidata_id)
    population = Population.objects.filter(wikidata_id=wikidata_id).order_by('year')
    area = Area.objects.filter(wikidata_id=wikidata_id).order_by('year')

    #filters
    population_2023 = Population.objects.filter(wikidata_id=wikidata_id, year=2023)
    population_2022 = Population.objects.filter(wikidata_id=wikidata_id, year=2022)
    population_none = Population.objects.filter(wikidata_id=wikidata_id, year__isnull=True)
    area_2023 = Area.objects.filter(wikidata_id=wikidata_id, year=2023)
    area_2022 = Area.objects.filter(wikidata_id=wikidata_id, year=2022)
    area_none = Area.objects.filter(wikidata_id=wikidata_id, year__isnull=True)

    if area_2023:
        area_filtered = area_2023[0]
    elif population_2022:
        area_filtered = area_2022[0]
    else:
        area_filtered = area_none[0]

    if population_2023:
        population_filtered = population_2023[0]
    elif population_2022:
        population_filtered = population_2022[0]
    else:
        population_filtered = population_none[0]
    
    context = {
        'entity': entity,
        'normdaten': normdaten,
        'wappen': wappen,
        'population': population,
        'area': area,
        'area_filtered': area_filtered,
        'population_filtered': population_filtered
    }

    return render(request, 'entity_detail.html', context)

def maps(request):
    return render(request, 'map.html')

def about(request):
    return render(request, 'about.html')
