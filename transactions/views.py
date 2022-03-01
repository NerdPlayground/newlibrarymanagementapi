from rest_framework import status
from students.models import Student
from transactions.models import Transaction
from rest_framework.response import Response
from rest_framework.decorators import APIView
from transactions.serializers import TransactionSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class TransactionAPIView(APIView):
    permission_classes= [IsAdminUser]
    def get(self,request):
        transactions= Transaction.objects.all()
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TransactionDetailAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        student= Student.objects.get(user=request.user)
        transactions= Transaction.objects.filter(student=student)
        serializer= TransactionSerializer(transactions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)