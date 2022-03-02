import datetime
from books.models import Book
from django.http import Http404
from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from authentication.serializers import RegisterSerializer,LoginSerializer,UserSerializer,RequestBookSerializer,IssueBookSerializer

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

class RequestBookAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def post(self,request):
        data= request.data
        serializer= RequestBookSerializer(data=data)
        if serializer.is_valid():
            transaction= Transaction.objects.create(
                student= Student.objects.get(user=request.user),
                book= Book.objects.get(id=request.data.get('book')),
            )
            transaction.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class IssueBookAPIView(APIView):
    permission_classes= [IsAdminUser]

    def get_object(self,pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def put(self,request,pk):
        transaction= self.get_object(pk)
        serializer= IssueBookSerializer(transaction,data=request.data)
        if serializer.is_valid():
            this_time= datetime.datetime.now()
            this_time= str(this_time).replace(" ","T") + "Z"
            serializer.save(issued_by=request.user,issued_at=this_time)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def delete(self,request):
        user= request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteDetailAPIView(APIView):
    permission_classes= [IsAdminUser]
    
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def delete(self,request,pk):
        student= self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)