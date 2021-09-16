from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('carbon', views.carbon, name='carbon'),
    path('ice', views.ice, name='ice'),
    path('ocean', views.ocean, name='ocean'),
]