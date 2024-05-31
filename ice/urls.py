from django.urls import path
from .views import AnchorTagInfoView, create_transmitter
from . import views
from .views import TransmitterAPIView


urlpatterns = [
    path('api/anchor-tag-info/', AnchorTagInfoView.as_view(), name='anchor-tag-info'),
    path('', views.anchor_tag_info, name='tag_info'),
    path('transmitters/', views.create_transmitter),
    path('transmitters/<str:transmitter_serial_number>/', TransmitterAPIView.as_view()),
]
