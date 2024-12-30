from django.urls import path
from . import views

urlpatterns = [
    path('', views.landkreise_list, name='landkreise_list'),  # Root-URL
    path('landkreise/<str:wikidata_id>/', views.landkreis_detail, name='landkreis_detail'),
]
