from django.http import Http404
from rest_framework import status
from students.models import Student
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework.generics import GenericAPIView
from library_cards.card_status import verify_patron
from rest_framework.permissions import IsAuthenticated
from notifications.serializers import NotificationSerializer

class NotificationsAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= NotificationSerializer
    
    def get(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                student= Student.objects.get(user=request.user)
                notifications= Notification.objects.filter(student=student)
                serializer= NotificationSerializer(notifications,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning":"Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class NotificationDetailAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= NotificationSerializer

    def get_object(self,pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        if not request.user.is_staff:
            if verify_patron(request=request):
                notification= self.get_object(pk=pk)
                serializer= NotificationSerializer(notification)
                notification.read= True
                notification.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning":"Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )
