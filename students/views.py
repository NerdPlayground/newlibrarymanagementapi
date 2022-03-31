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
from library_cards.card_status import verify_patron
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from students.serializers import UpdateSerializer,StudentSerializer,BookItemSerializer

class UpdateAPIView(GenericAPIView):
    serializer_class= UpdateSerializer
    permission_classes= [IsAuthenticated]

    def put(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                student= Student.objects.get(user=request.user)
                serializer= UpdateSerializer(student,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class StudentsAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= StudentSerializer

    def get(self,request):
        students= Student.objects.all()
        serializer= StudentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class StudentDetailAPIView(GenericAPIView):
    serializer_class= StudentSerializer
    permission_classes= [IsAuthenticated]
    
    def get(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                student= Student.objects.get(user=request.user)
                serializer= StudentSerializer(student)
                self.books_checked_out(student=student)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CheckOutBookItemAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= BookItemSerializer

    def book_items_checked_out(self,student):
        book_items= BookItem.objects.filter(loaned_to=student)
        return len(book_items)

    def checkout(self,student,book_item,due_date,available):
        book_item.status= "Loaned"
        book_item.loaned_to= student
        if not available:
            book_item.reserved_by= None
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

    def post(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                book_item= BookItem.objects.get(id=request.data.get("book_item"))
                student= Student.objects.get(user=request.user)
                due_date= datetime.date.today()+datetime.timedelta(days=5)
                serializer= BookItemSerializer(data=request.data)

                if serializer.is_valid():
                    if not book_item.reference:
                        if book_item.status == "Available":
                            if self.book_items_checked_out(student=student) < 5:
                                self.checkout(student,book_item,due_date,True)
                                serializer.save(
                                    student= student,
                                    due_date= due_date
                                )
                                return Response(serializer.data,status=status.HTTP_201_CREATED)
                            else:
                                return Response(
                                    {"message":"Can't check out more than five book items"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )

                        elif book_item.status == "Loaned":
                            if book_item.loaned_to != student:
                                Reservation.objects.create(
                                    student= student,
                                    book_item= book_item
                                )

                                book_item.status = "Reserved"
                                book_item.reserved_by= student
                                book_item.save()

                                return Response(
                                    {"message":"This book item is loaned and it has been added to your reservations"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            else:
                                return Response(
                                    {"message":"Student loaned to and current user match"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        
                        elif book_item.status == "Reserved":
                            if book_item.reserved_by == student:
                                self.checkout(student,book_item,due_date,False)
                                serializer.save(
                                    student= student,
                                    due_date= due_date
                                )
                                
                                reservation= Reservation.objects.get(
                                    student= student,
                                    book_item= book_item,
                                    status= "Pending"
                                )
                                reservation.status = "Completed"
                                reservation.save()

                                return Response(
                                    serializer.data,
                                    status=status.HTTP_201_CREATED
                                )
                            else:
                                return Response(
                                    {"message":"This Book Item is Resereved"},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        
                    else:
                        return Response(
                            {"message":"This is a Reference Book Item"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class ReturnBookItemAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= BookItemSerializer

    def post(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                book_item= BookItem.objects.get(id=request.data.get('book_item'))
                student= Student.objects.get(user=request.user)
                message= "Book item successfully returned. Thank you for reading with us"
                serializer= BookItemSerializer(data=request.data)

                if serializer.is_valid():
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
                        transaction.returned= True
                        transaction.returned_at= datetime.date.today()
                        transaction.save()
                        return Response(
                            {"message": message},
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {"Warning":"Student loaned to and current user don't match"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator access denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class RenewBookItemAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= BookItemSerializer

    def post(self,request):
        if not request.user.is_staff:
            if verify_patron(request=request):
                book_item= BookItem.objects.get(id=request.data.get('book_item'))
                student= Student.objects.get(user=request.user)
                other_message= str()
                message= "Book item successfully renewed. Thank you for reading with us."
                serializer= BookItemSerializer(data=request.data)

                if serializer.is_valid():
                    if student == book_item.loaned_to:
                        if book_item.status != "Reserved":
                            transaction= Transaction.objects.get(book_item=book_item,returned_at=None)
                            if transaction.due_date < datetime.date.today():
                                library_card= LibraryCard.objects.get(student=student)
                                library_card.active= False
                                library_card.save()
                                other_message= "Note: Pay existing fine to actvate library card."
                            transaction.due_date += datetime.timedelta(days=5)
                            transaction.save()

                            name= transaction.book_item.book.name
                            due_date= transaction.due_date
                            notification= Notification.objects.create(
                                student= student,
                                title= "Transaction Renewal",
                                message= "You have renewed your transaction for" 
                                +" book item ("+name +")"
                                +". Ensure the book item is returned or"
                                +" your transaction is renewed"
                                +" before or on " +str(due_date)
                                +" to avoid revocation of your library card."
                            )
                            notification.save()

                            return Response(
                                {"Message":message +" " +other_message},
                                status=status.HTTP_200_OK
                            )
                        else:
                            return Response(
                                {"message":"This book item is resereved."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {"Warning":"Student loaned to and current user don't match"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning: Administrator Access Denied"},
                status=status.HTTP_401_UNAUTHORIZED
            )