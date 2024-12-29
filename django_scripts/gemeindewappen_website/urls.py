from django.urls import path
from . import views

urlpatterns = [
    path('', views.wappen_list, name='wappen_list'),
]
