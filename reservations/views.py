from django.http import Http404
from rest_framework import status
from students.models import Student
from reservations.models import Reservation
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from library_cards.card_status import verify_patron
from rest_framework.permissions import IsAuthenticated
from reservations.serializers import ReservationSerializer

class PatronReservationsAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= ReservationSerializer
    
    def get(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                try:
                    student= Student.objects.get(user=request.user)
                    reservations= Reservation.objects.filter(student=student)
                    serializer= ReservationSerializer(reservations,many=True)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                except Reservation.DoesNotExist:
                    return Response(
                        {"message":"No reservations made"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CancelReservationAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= ReservationSerializer

    def get_object(self,pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404
    
    def delete(self,request,pk):
        if not request.user.is_staff:
            if verify_patron(request=request):
                reservation= self.get_object(pk)
                book_item= reservation.book_item
                book_item.status= "Loaned"
                book_item.reserved_by= None
                book_item.save()
                reservation.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )
