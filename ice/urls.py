from django.urls import path
from .views import  create_transmitter, status_log_view
from . import views
from django.conf.urls import handler404





urlpatterns = [


    path('transmitters/', views.create_transmitter),
    path('', views.transmitter_list),
    path('delete/<str:device_uid>/', views.delete_read, name='delete_read'),
    path('status-logs/', status_log_view, name='status_log_view'),
]

handler404 = 'ice.views.custom_404_view'
