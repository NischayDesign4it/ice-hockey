from django.urls import path
from .views import  create_transmitter
from . import views


urlpatterns = [


    path('transmitters/', views.create_transmitter),
    path('', views.transmitter_list),
]
