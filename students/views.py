from django.http import Http404
from rest_framework import status
from students.models import Student
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from students.serializers import UpdateSerializer,StudentSerializer

class UpdateAPIView(GenericAPIView):
    serializer_class= UpdateSerializer
    permission_classes= [IsAuthenticated]
    def put(self,request):
        if not request.user.is_staff:
                student= Student.objects.get(user=request.user)
                serializer= UpdateSerializer(student,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)

class StudentAPIView(GenericAPIView):
    serializer_class= StudentSerializer
    permission_classes= [IsAdminUser]
    def get(self,request):
        students= Student.objects.all()
        serializer= StudentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class StudentDetailAPIView(GenericAPIView):
    serializer_class= StudentSerializer
    permission_classes= [IsAuthenticated]
    def get(self,request):
        if not request.user.is_staff:
            student= Student.objects.get(user=request.user)
            serializer= StudentSerializer(student)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)