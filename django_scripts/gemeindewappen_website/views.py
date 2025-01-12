from django.shortcuts import render
from django.db.models import Max
from .models import *
from django.db.models import Q
import random

# Create your views here.

def entity_list(request):
    entities = Entity.objects.order_by('name')
    random_wappen = random.choice(Wappen.objects.all())
    return render(request, 'frontpage.html', {'entities': entities, 'random_wappen': random_wappen})

def entity_detail(request, wikidata_id):
    entity = Entity.objects.get(wikidata_id=wikidata_id)
    normdaten = Normdaten.objects.get(wikidata_id=wikidata_id)
    wappen = Wappen.objects.get(wikidata_id=wikidata_id)
    population = Population.objects.filter(wikidata_id=wikidata_id).order_by('year')
    population_filter = Population.objects.filter(wikidata_id=wikidata_id).order_by('-year')
    area = Area.objects.filter(wikidata_id=wikidata_id).order_by('-year')
    area_filter = Area.objects.filter(wikidata_id=wikidata_id).order_by('-year')

    #filters
    # area_2023 = Area.objects.filter(wikidata_id=wikidata_id, year=2023)
    # area_2022 = Area.objects.filter(wikidata_id=wikidata_id, year=2022)
    # area_none = Area.objects.filter(wikidata_id=wikidata_id, year__isnull=True)

    # if area_2023:
    #     area_filtered = area_2023[0]
    # elif area_2022:
    #     area_filtered = area_2022[0]
    # else:
    #     area_filtered = area_none[0]

    context = {
        'entity': entity,
        'normdaten': normdaten,
        'wappen': wappen,
        'population': population,
        'area': area,
        'area_filtered': area_filter[0],
        'population_filter': population_filter[0]
    }

    return render(request, 'entity_detail.html', context)

def maps(request):
    return render(request, 'map.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        results = Entity.objects.filter(
            Q(name__icontains=query)
        )
    else:
        results = Entity.objects.all()
    
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'search_results.html', context)

def coa_list(request):
    entities = Entity.objects.order_by('name')
    return render(request, 'coa_list.html', {'entities': entities})
