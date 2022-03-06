from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from transactions.serializers import TransactionSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class TransactionAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAdminUser]
    def get(self,request):
        transactions= Transaction.objects.all()
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TransactionDetailAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAuthenticated]
    def get(self,request):
        student= Student.objects.get(user=request.user)
        transactions= Transaction.objects.filter(student=student)
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RequestedBooksAPIView(GenericAPIView):
    serializer_class= TransactionSerializer
    permission_classes= [IsAdminUser]
    def get(self,request):
        transactions= Transaction.objects.filter(issued=False)
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
            