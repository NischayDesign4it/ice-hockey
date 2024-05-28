from django.urls import path
from .views import AnchorTagInfoView

urlpatterns = [
    path('api/anchor-tag-info/', AnchorTagInfoView.as_view(), name='anchor-tag-info')
]
