from django.urls import path
from fines.views import FineAPIView,FineDetailAPIView

urlpatterns= [
    path('all-fines/',FineAPIView.as_view(),name='all-fines'),
    path('my-fines/',FineDetailAPIView.as_view(),name='my-fines'),
]