from rest_framework import status
from students.models import Student
from rest_framework.response import Response
from rest_framework.decorators import APIView
from students.serializers import UpdateSerializer,StudentSerializer

class UpdateAPIView(APIView):
    def put(self,request):
        student= Student.objects.get(id=request.data.get('id'))
        serializer= UpdateSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentAPIView(APIView):
    def get(self,request):
        students= Student.objects.all()
        serializer= StudentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)