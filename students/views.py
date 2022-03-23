import datetime
from fines.models import Fine
from django.http import Http404
from rest_framework import status
from students.models import Student
from book_items.models import BookItem
from transactions.models import Transaction
from reservations.models import Reservation
from rest_framework.response import Response
from library_cards.models import LibraryCard
from notifications.models import Notification
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
            due_date= datetime.date.today()+datetime.timedelta(days=5)
            serializer= CheckOutBookItemSerializer(data=request.data)

            if serializer.is_valid():
                if not book_item.reference:
                    if book_item.status == "Available":
                        serializer.save(
                            student= student,
                            due_date= due_date
                        )
                        book_item.status= "Loaned"
                        book_item.loaned_to= student
                        book_item.save()

                        name= book_item.book.name
                        notification= Notification.objects.create(
                            student= student,
                            title= "Book Lending",
                            message= "You have checked out " +name
                            +". Ensure the book item is returned or"
                            +" your transaction is renewed"
                            +" before or on " +str(due_date)
                            +" to avoid revocation of your library card."
                        )
                        notification.save()

                        return Response(serializer.data,status=status.HTTP_201_CREATED)

                    elif book_item.status == "Loaned":
                        Reservation.objects.create(
                            student= student,
                            book_item= book_item
                        )

                        book_item.status = "Reserved"
                        book_item.reserved_by= student
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
    permission_classes= [IsAuthenticated]
    def post(self,request):
        book_item= BookItem.objects.get(id=request.data.get('book_item'))
        student= Student.objects.get(user=request.user)
        message= "Book item successfully returned. Thank you for reading with us"
        if student == book_item.loaned_to:
            transaction= Transaction.objects.get(book_item=book_item,returned_at=None)
            if transaction.due_date < datetime.date.today():
                library_card= LibraryCard.objects.get(student=student)
                library_card.active= False
                library_card.save()
                message= "Pay existing fine to actvate library card"

            book_item.loaned_to= None
            if book_item.reserved_by is not None:
                name= book_item.book.name
                notification= Notification.objects.create(
                    student= book_item.reserved_by,
                    title= "Reserved Book",
                    message= name+" is available for checkout."
                )
                notification.save()
            else:
                book_item.status= "Available"
            book_item.save()
            transaction.returned_at= datetime.date.today()
            transaction.save()
            return Response({"message": message},status=status.HTTP_200_OK)
        else:
            return Response({"Warning":"Student loaned to and current user don't match"})

class RenewBookItemAPIView(GenericAPIView):
    def post(self,request):
        pass

class ModifyTransactionAPIView(GenericAPIView):
    def get(self,request):
        transaction= Transaction.objects.get(id=19)
        transaction.issued_at= datetime.date.today()-datetime.timedelta(days=8)
        transaction.due_date= datetime.date.today()-datetime.timedelta(days=3)
        transaction.save()
        return Response(status=status.HTTP_200_OK)
