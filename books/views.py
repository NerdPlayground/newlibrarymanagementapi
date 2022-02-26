from books.models import Book
from rest_framework import status
from rest_framework.response import Response
from books.serializers import BookSerializer
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser

class AddBookAPIView(APIView):
    def post(self,request):
        serializer= BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewBooksAPIView(APIView):
    def get(self,request):
        categories= Book.objects.all()
        serializer= BookSerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditBooksAPIView(APIView):
    def get_object(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        category= self.get_object(pk)
        serializer= BookSerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        category= self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)