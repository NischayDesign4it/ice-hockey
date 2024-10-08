from django.urls import path
from .views import  create_transmitter
from . import views
from django.conf.urls import handler404





urlpatterns = [


    path('transmitters/', views.create_transmitter),
    path('', views.transmitter_list),
    path('delete/<str:device_uid>/', views.delete_read, name='delete_read'),
]

handler404 = 'ice.views.custom_404_view'
