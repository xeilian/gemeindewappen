from django.urls import path
from . import views

urlpatterns = [
    path('', views.entity_list, name='entity_list'), 
    path('entity/<str:wikidata_id>/', views.entity_detail, name='entity_detail'),
    path('map/', views.maps, name='map'),
]
