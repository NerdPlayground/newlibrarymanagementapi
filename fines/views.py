import datetime
from fines.models import Fine
from django.http import Http404
from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from fines.serializers import FineSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class UpdatePatronFinesAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= [FineSerializer]

    def get_object(self,loaned_book):
        today= datetime.date.today()
        try:
            return (Fine.objects.get(transaction=loaned_book),True,)
        except Fine.DoesNotExist:
            fine= Fine.objects.create(
                transaction= loaned_book,
                amount= (today-loaned_book.due_date).days * 50,
            )
            return (fine,False,)

    def get(self,request):
        today= datetime.date.today()
        loaned_books= Transaction.objects.filter(returned_at=None,due_date__lt=today)
        for loaned_book in loaned_books:
            retrieved_fine= self.get_object(loaned_book)
            if retrieved_fine[1]:
                fine= retrieved_fine[0]
                fine.amount= (today-loaned_book.due_date).days * 50
                fine.save()
        
        return Response({"message":"Library fines have been updated."},status=status.HTTP_200_OK)

class FineAPIView(GenericAPIView):
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

# class PayFineAPIView(GenericAPIView):
#     permission_classes= [IsAuthenticated]
#     def get_object(self,pk):
#         try:
#             return Fine.objects.get(pk=pk)
#         except Fine.DoesNotExist:
#             raise Http404
    
#     def post(self,request,pk):
#         fine= self.get_object(pk=pk)
#         amount= request.data.get('amount')

#         if amount < fine.amount:
#             return Response({"Fine":fine.amount,"Message":"Please pay the full amount"},status=status.HTTP_200_OK)
#         else:
#             fine.paid_on= datetime.date.today()
#             fine.save()
#             return Response({"Message":"Thank you for clearing your fine."},status=status.HTTP_200_OK)