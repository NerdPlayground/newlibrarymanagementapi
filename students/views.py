from django.http import Http404
from rest_framework import status
from students.models import Student
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from students.serializers import UpdateSerializer,StudentSerializer

class UpdateAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request):
        if not request.user.is_staff:
                student= Student.objects.get(id=request.user.id)
                serializer= UpdateSerializer(student,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)

class StudentAPIView(APIView):
    permission_classes= [IsAdminUser]
    def get(self,request):
        students= Student.objects.all()
        serializer= StudentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class StudentDetailAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        if not request.user.is_staff:
            student= Student.objects.get(user=request.user)
            serializer= StudentSerializer(student)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)