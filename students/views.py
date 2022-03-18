import datetime
from django.http import Http404
from rest_framework import status
from students.models import Student
from book_items.models import BookItem
from reservations.models import Reservation
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from students.serializers import UpdateSerializer,StudentSerializer,CheckOutBookItemSerializer

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

class CheckOutBookItemAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= [CheckOutBookItemSerializer]

    def post(self,request):
        if not request.user.is_staff:
            book_item= BookItem.objects.get(id=request.data.get("book_item"))
            student= Student.objects.get(user=request.user)
            serializer= CheckOutBookItemSerializer(data=request.data)

            if serializer.is_valid():
                if not book_item.reference:
                    if book_item.status == "Available":
                        serializer.save(
                            student= Student.objects.get(user=request.user),
                            due_date= datetime.date.today()+datetime.timedelta(days=5)
                        )
                        book_item.status= "Loaned"
                        book_item.save()
                        return Response(serializer.data,status=status.HTTP_201_CREATED)

                    elif book_item.status == "Loaned":
                        Reservation.objects.create(
                            student= student,
                            book_item= book_item
                        )

                        book_item.status = "Reserved"
                        book_item.save()

                        return Response(
                            {
                                "message":
                                [
                                    "This book item is loaned",
                                    "This book item has been added to your reservations"
                                ]
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    elif book_item.status == "Reserved":
                        return Response({"message":"This Book Item is Resereved"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"This is a Reference Book Item"},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Warning: Administrator Access Denied"},status=status.HTTP_401_UNAUTHORIZED)

class ReturnBookItemAPIView(GenericAPIView):
    def post(self,request):
        pass

class RenewBookItemAPIView(GenericAPIView):
    def post(self,request):
        pass