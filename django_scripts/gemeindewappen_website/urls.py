from django.urls import path
from . import views

urlpatterns = [
    path('', views.landkreise_list, name='landkreise_list'),
    path('landkreis/<int:id>/', views.landkreis_detail, name='landkreis_detail'),
]
