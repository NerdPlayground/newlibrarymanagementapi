from django.urls import path
from fines.views import FinesAPIView,FineDetailAPIView,UpdatePatronFinesAPIView,PayFineAPIView

urlpatterns= [
    path('all-fines/',FinesAPIView.as_view(),name='all-fines'),
    path('my-fines/',FineDetailAPIView.as_view(),name='my-fines'),
    path('pay-fine/<str:pk>/',PayFineAPIView.as_view(),name='pay-fine'),
    path('update-fines/',UpdatePatronFinesAPIView.as_view(),name='update-fines')
]