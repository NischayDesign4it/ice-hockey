from django.urls import path
from .views import AnchorTagInfoView
from . import views

urlpatterns = [
    path('api/anchor-tag-info/', AnchorTagInfoView.as_view(), name='anchor-tag-info'),
    path('', views.anchor_tag_info, name='tag_info'),
]
