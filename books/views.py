from datetime import date
from books.models import Book
from racks.models import Rack
from django.http import Http404
from rest_framework import status
from book_items.models import BookItem
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from books.serializers import BookSerializer,ViewBookSerializer

class AddBookAPIView(GenericAPIView):
    serializer_class= BookSerializer
    permission_classes= [IsAdminUser]
    
    def add_book_items(self,book,published_on,quantity,rack):
        while quantity != 0:
            BookItem.objects.create(
                book= book,
                reference= False,
                status= "Available",
                purchased_on= date.today(),
                published_on= published_on,
                rack= rack
            )
            quantity -= 1

    def post(self,request):
        quantity= request.data.get('quantity')
        rack= request.data.get('rack')

        if quantity == None:
            return Response(
                {"quantity":["This field is required"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif quantity < 1:
            return Response(
                {"quantity":["This field should be at least 1"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if rack == None:
            return Response(
                {"rack":["This field is required"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif rack == "":
            return Response(
                {"rack":["This field should have a valid identifier"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer= BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.add_book_items(
                book= Book.objects.get(isbn=request.data.get('isbn')),
                published_on= request.data.get('published_on'),
                quantity= quantity,
                rack= Rack.objects.get(id=request.data.get('rack'))
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewBooksAPIView(GenericAPIView):
    serializer_class= ViewBookSerializer
    def get(self,request):
        categories= Book.objects.all()
        serializer= ViewBookSerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

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

class EditBookAPIView(GenericAPIView):
    serializer_class= BookSerializer
    permission_classes= [IsAdminUser]

    def get_object(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    
    def put(self,request,pk):
        book= self.get_object(pk)
        serializer= BookSerializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        book= self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)