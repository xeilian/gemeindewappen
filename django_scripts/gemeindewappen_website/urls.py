from django.urls import path
from . import views

urlpatterns = [
    path('', views.entity_list, name='entity_list'), 
    path('entity/<str:wikidata_id>/', views.entity_detail, name='entity_detail'),
    path('map/', views.maps, name='map'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('coa_list/', views.coa_list, name='coa_list')
]
