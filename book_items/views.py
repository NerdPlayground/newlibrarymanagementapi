from datetime import date
from django.http import Http404
from rest_framework import status
from book_items.models import BookItem
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from book_items.serializers import BookItemSerializer

class BookItemAPIView(GenericAPIView):
    serializer= BookItemSerializer
    def get(self,request):
        book_items= BookItem.objects.all()
        serializer= BookItemSerializer(book_items,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer= BookItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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

    def put(self,request,pk):
        book_item= self.get_object(pk)
        serializer= BookItemSerializer(book_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)