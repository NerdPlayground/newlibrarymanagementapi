import datetime
from fines.models import Fine
from django.http import Http404
from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from rest_framework.response import Response
from library_cards.models import LibraryCard
from notifications.models import Notification
from rest_framework.generics import GenericAPIView
from fines.serializers import FineSerializer,PayFineSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class UpdatePatronFinesAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= [FineSerializer]

    def __init__(self):
        self.today= datetime.date.today()

    def get_object(self,loaned_book,amount):
        try:
            return (Fine.objects.get(transaction=loaned_book),True,)
        except Fine.DoesNotExist:
            loaned_book.overdue= True
            loaned_book.save()
            fine= Fine.objects.create(
                transaction= loaned_book,
                amount= amount,
                last_updated= datetime.date.today()
            )
            return (fine,False,)

    def get(self,request):
        loaned_books= Transaction.objects.filter(returned_at=None,due_date__lt=self.today)
        for loaned_book in loaned_books:
            amount= (self.today-loaned_book.due_date).days * 50
            retrieved_fine= self.get_object(
                loaned_book= loaned_book,
                amount= amount
            )
            
            if retrieved_fine[1]:
                fine= retrieved_fine[0]
                fine.amount= amount
                fine.last_updated= datetime.date.today()
                fine.save()
            
            notification= Notification.objects.create(
                student= loaned_book.student,
                title= "Overdue Book",
                message= "The book item (" 
                +loaned_book.book_item.book.name +")"
                +" is overdue. You are required to return"
                +" the book item and pay the incurred fine."
                +" Fine: " +str(amount) +" Kenyan Shillings"
            )
            notification.save()
        
        return Response(
            {"message":"Library fines have been updated."},
            status=status.HTTP_200_OK
        )

class FinesAPIView(GenericAPIView):
    serializer_class= FineSerializer
    permission_classes= [IsAdminUser]

    def get(self,request):
        fines= Fine.objects.all()
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FineDetailAPIView(GenericAPIView):
    serializer_class= FineSerializer
    permission_classes= [IsAuthenticated]

    def get_object(self,transaction):
        try:
            return (Fine.objects.get(transaction=transaction),True,)
        except Fine.DoesNotExist:
            return (None,False,)

    def get(self,request):
        student= Student.objects.get(user=request.user)
        transactions= Transaction.objects.filter(student=student)
        fines= list()
        for transaction in transactions:
            fine= self.get_object(transaction)
            if fine[1]:
                fines.append(fine[0])
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PayFineAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= PayFineSerializer

    def get_object(self,pk):
        try:
            return Fine.objects.get(pk=pk)
        except Fine.DoesNotExist:
            raise Http404
    
    def post(self,request,pk):
        fine= self.get_object(pk=pk)
        amount= request.data.get('amount')
        serializer= PayFineSerializer(amount)
        if serializer.is_valid():
            if amount < fine.amount:
                return Response(
                    {
                        "Fine":fine.amount,
                        "Message":"Please pay the full amount"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                fine.paid= True
                fine.paid_on= datetime.date.today()
                fine.save()
                library_card= LibraryCard.objects.get(student=fine.transaction.student)
                library_card.active= True
                library_card.save()
                return Response(
                    {"Message":"Thank you for clearing your fine."},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)