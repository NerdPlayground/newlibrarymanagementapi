from django.urls import path
from racks.views import AddRackAPIView,ViewRacksAPIView

urlpatterns= [
    path('racks/',ViewRacksAPIView.as_view(),name='racks'),
    path('add-rack/',AddRackAPIView.as_view(),name='add-rack'),
]