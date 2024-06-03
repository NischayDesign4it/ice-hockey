from django.urls import path
from .views import  create_transmitter
from . import views


urlpatterns = [


    path('/transmitters/?apiKey=default-api-key', views.create_transmitter),
    path('', views.transmitter_list),
]
