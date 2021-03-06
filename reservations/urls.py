from django.urls import path
from reservations.views import PatronReservationsAPIView,CancelReservationAPIView

urlpatterns= [
    path('reservations/',PatronReservationsAPIView.as_view(),name='reservations'),
    path('cancel-reservation/<str:pk>/',CancelReservationAPIView.as_view(),name='cancel-reservation'),
]