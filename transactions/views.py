from django.http import Http404
from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from library_cards.card_status import verify_patron
from transactions.serializers import TransactionSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class LibraryTransactionsAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAdminUser]
    
    def get(self,request):
        transactions= Transaction.objects.all()
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PatronTransactionsAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAuthenticated]

    def get(self,request):
        if verify_patron(request=request):
            student= Student.objects.get(user=request.user)
            transactions= Transaction.objects.filter(student=student)
            serializer= TransactionSerializer(transactions,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(
                {"message":"Library card has been revoked"},
                status=status.HTTP_400_BAD_REQUEST
            )

class TransactionDetailAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        if verify_patron(request=request):
            transaction= self.get_object(pk=pk)
            serializer= TransactionSerializer(transaction)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(
                {"message":"Library card has been revoked"},
                status=status.HTTP_400_BAD_REQUEST
            )