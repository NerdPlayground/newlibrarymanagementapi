import datetime
from books.models import Book
from django.http import Http404
from rest_framework import status
from book_items.models import BookItem
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from book_items.serializers import BookItemSerializer,EditBookItemSerializer

class AddBookItemAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= BookItemSerializer

    def post(self,request):
        serializer= BookItemSerializer(data=request.data)
        if serializer.is_valid():
            book= Book.objects.get(id=request.data.get('book'))
            serializer.save(
                status= "Available",
                purchased_on= datetime.date.today(),
                published_on= book.published_on
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BookItemsAPIView(GenericAPIView):
    serializer_class= BookItemSerializer

    def get(self,request):
        book_id= request.data.get('book_id')
        if book_id == None or book_id == "":
            return Response(
                {"book_id":["This field is required"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            book_items= BookItem.objects.filter(book=book_id)
            serializer= BookItemSerializer(book_items,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

class BookItemDetailAPIView(GenericAPIView):
    serializer_class= BookItemSerializer

    def get_object(self,pk):
        try:
            return BookItem.objects.get(pk=pk)
        except BookItem.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        book_item= self.get_object(pk)
        serializer= BookItemSerializer(book_item)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditBookItemAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= EditBookItemSerializer

    def get_object(self,pk):
        try:
            return BookItem.objects.get(pk=pk)
        except BookItem.DoesNotExist:
            raise Http404
    
    def put(self,request,pk):
        book_item= self.get_object(pk)
        serializer= EditBookItemSerializer(book_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        book_item= self.get_object(pk)
        book_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)