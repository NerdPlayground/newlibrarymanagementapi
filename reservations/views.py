from django.http import Http404
from rest_framework import status
from students.models import Student
from reservations.models import Reservation
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from reservations.serializers import ReservationSerializer

class PatronReservationsAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= [ReservationSerializer]
    
    def get(self,request):
        try:
            student= Student.objects.get(user=request.user)
            reservations= Reservation.objects.get(student=student)
            serializer= ReservationSerializer(reservations)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"message":"No Reservations Made"},status=status.HTTP_404_NOT_FOUND)

class CancelReservationAPIView(GenericAPIView):
    serializer_class= [ReservationSerializer]
    permission_classes= [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404
    
    def put(self,request,pk):
        reservation= self.get_object(pk)
        serializer= ReservationSerializer(reservation,data=request)
        if serializer.is_valid():
            serializer.save(status="Cancel")
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)