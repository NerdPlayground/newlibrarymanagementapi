from django.urls import path
from racks.views import AddRackAPIView,ViewRackAPIView

urlpatterns= [
    path('racks/',ViewRackAPIView.as_view(),name='rack'),
    path('racks/add/',AddRackAPIView.as_view(),name='add-rack'),
]