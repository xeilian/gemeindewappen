from django.shortcuts import render
from .models import *
from django.db.models import Q
import random

def entity_list(request):
    entities = Entity.objects.filter(online='x').order_by('name')
    wappen = Wappen.objects.filter(wikidata_id__in=entities.values_list('wikidata_id', flat=True))
    random_wappen = random.choice(wappen)
    return render(request, 'frontpage.html', {'entities': entities, 'random_wappen': random_wappen})

def entity_detail(request, wikidata_id):
    entity = Entity.objects.get(wikidata_id=wikidata_id)
    normdaten = Normdaten.objects.get(wikidata_id=wikidata_id)
    wappen = Wappen.objects.get(wikidata_id=wikidata_id)
    population = Population.objects.filter(wikidata_id=wikidata_id).order_by('year')
    population_filter = Population.objects.filter(wikidata_id=wikidata_id).order_by('-year')
    area = Area.objects.filter(wikidata_id=wikidata_id).order_by('-year')
    area_filter = Area.objects.filter(wikidata_id=wikidata_id).order_by('-year')

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
