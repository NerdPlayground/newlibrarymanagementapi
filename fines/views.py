import datetime
from fines.models import Fine
from django.http import Http404
from rest_framework import status
from students.models import Student
from fines.serializers import FineSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class FineAPIView(APIView):
    permission_classes= [IsAdminUser]
    def get(self,request):
        fines= Fine.objects.all()
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FineDetailAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        student= Student.objects.get(user=request.user)
        fines= Fine.objects.filter(student=student)
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
