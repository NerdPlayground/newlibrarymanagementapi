import datetime
from fines.models import Fine
from books.models import Book
from django.http import Http404
from rest_framework import status
from students.models import Student
from django.db.models.query import QuerySet
from transactions.models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from authentication.serializers import (
    RegisterSerializer,LoginSerializer,UserSerializer,
    RequestBookSerializer,IssueBookSerializer,PossessedBooksSerializer
)

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
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

class LoginAPIView(GenericAPIView):
    def post(self,request):
        username= request.data.get('username')
        password= request.data.get('password')
        user= authenticate(username=username,password=password)

        if user is not None:
            serializer= LoginSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_401_UNAUTHORIZED)

class UserAPIView(GenericAPIView):
    def get(self,request):
        users= User.objects.all()
        serializer= UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RequestBookAPIView(GenericAPIView):
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

class IssueBookAPIView(GenericAPIView):
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
            # this_time= datetime.datetime.now()
            # this_time= str(this_time).replace(" ","T") + "Z"
            this_time= "2022-03-02T15:53:01.946805Z"
            serializer.save(issued_by=request.user,issued_at=this_time)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PossessedBooksAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        if not request.user.is_staff:
            student= Student.objects.get(user=request.user)
            transactions= Transaction.objects.filter(student=student)
            issued_transactions= transactions.filter(issued=True)
            books= list()
            for transaction in issued_transactions:
                books.append(transaction.book)
            serializer= PossessedBooksSerializer(books,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)

class DueBooksAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    def difference(self,issued_at):
        today,then= int(datetime.datetime.now().strftime("%d")),int(issued_at.strftime("%d"))
        this_month,last_month= int(datetime.datetime.now().strftime("%m")),int(issued_at.strftime("%m"))
        this_year,last_year= int(datetime.datetime.now().strftime("%Y")),int(issued_at.strftime("%Y"))

        if int(this_year != last_year):
            days_till_end= int()
            days_till_now= int()
            days_of_months= [31,28,31,30,31,30,31,31,30,31,30,31]
            if last_year%4 == 0:
                days_of_months[1]= 29
            
            if last_month == 12:
                days_till_end= 31-then
            else:
                for days in range(last_month,12):
                    days_till_end += days_of_months[days]
                days_till_end += (last_month-then)
            
            if this_month == 1:
                days_till_now += today
            else:
                for days in range(0,this_month-1):
                    days_till_now += days_of_months[days]
                days_till_now += today
            
            return days_till_end+days_till_now

        elif int(this_month != last_month):
            last_month_days= (
                31 if last_month in [1,3,5,7,8,10,12]
                else 28 if last_month is 2 and last_year % 4 == 0
                else 30
            )
            return last_month_days+today-then

        else:
            return int(today)-int(then)
    
    def get(self,request):
        if not request.user.is_staff:
            student= Student.objects.get(user=request.user)
            transactions= Transaction.objects.filter(student=student)
            retained_transactions= transactions.filter(returned=False)
            books= list()

            for transaction in retained_transactions:
                time_difference= self.difference(transaction.issued_at)
                if time_difference > 1:
                    books.append(transaction.book)
                    fine= Fine.objects.get_or_create(
                        student= student,
                        transaction= transaction,
                        amount= time_difference * 50
                    )

            serializer= PossessedBooksSerializer(books,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)

class DeleteAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    def delete(self,request):
        user= request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteDetailAPIView(GenericAPIView):
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