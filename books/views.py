from datetime import date
from books.models import Book
from rest_framework import status
from book_items.models import BookItem
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from django.http import Http404,HttpResponseBadRequest
from books.serializers import BookSerializer,ViewBookSerializer

class AddBookAPIView(GenericAPIView):
    serializer_class= BookSerializer
    def add_book_items(self,book,published_on,quantity):
        while quantity != 0:
            BookItem.objects.create(
                book= book,
                reference= False,
                status= "Available",
                purchased_on= date.today(),
                published_on= published_on
            )
            quantity -= 1

    def post(self,request):
        quantity= request.data.get('quantity')
        if quantity == None:
            return Response({"quantity":["This field is required"]},status=status.HTTP_400_BAD_REQUEST)
        
        serializer= BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.add_book_items(
                book= Book.objects.get(isbn=request.data.get('isbn')),
                published_on= request.data.get('published_on'),
                quantity= quantity,
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewBookAPIView(GenericAPIView):
    serializer_class= ViewBookSerializer
    def get_object(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        book= self.get_object(pk)
        serializer= ViewBookSerializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ViewBooksAPIView(GenericAPIView):
    serializer_class= ViewBookSerializer
    def get(self,request):
        categories= Book.objects.all()
        serializer= ViewBookSerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditBookAPIView(GenericAPIView):
    serializer_class= BookSerializer
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