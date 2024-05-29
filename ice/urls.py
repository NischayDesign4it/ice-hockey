from django.urls import path
from .views import AnchorTagInfoView
from . import views

urlpatterns = [
    path('api/anchor-tag-info/', AnchorTagInfoView.as_view(), name='anchor-tag-info'),
    path('tag-info/', views.anchor_tag_info, name='tag_info'),
]
