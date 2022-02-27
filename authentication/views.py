from rest_framework import status
from students.models import Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import APIView
from authentication.serializers import RegisterSerializer,LoginSerializer,UserSerializer

class RegisterAPIView(APIView):
    def post(self,request):
        serializer= RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                first_name= request.data.get('first_name'),
                last_name= request.data.get('last_name'),
                username= request.data.get('username'),
                email= request.data.get('email')
            )
            user.set_password(request.data.get('password'))
            user.save()
            
            student= Student.objects.create(
                user= user,
                first_name= user.first_name,
                last_name= user.last_name
            )
            student.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self,request):
        username= request.data.get('username')
        password= request.data.get('password')
        user= authenticate(username=username,password=password)

        if user is not None:
            serializer= LoginSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_401_UNAUTHORIZED)

class UserAPIView(APIView):
    def get(self,request):
        users= User.objects.all()
        serializer= UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)