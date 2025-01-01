from django.urls import path
from . import views

urlpatterns = [
    path('', views.landkreise_list, name='landkreise_list'), 
    path('landkreise/<str:wikidata_id>/', views.landkreis_detail, name='landkreis_detail'),
    path('map/', views.maps, name='map')
]
