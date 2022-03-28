from django.http import Http404
from rest_framework import status
from categories.models import Category
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from categories.serializers import CategorySerializer,ViewCategorySerializer

class AddCategoryAPIView(GenericAPIView):
    serializer_class= CategorySerializer
    permission_classes = [IsAdminUser]

    def post(self,request):
        serializer= CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewCategoriesAPIView(GenericAPIView):
    serializer_class= ViewCategorySerializer
    def get(self,request):
        categories= Category.objects.all()
        serializer= ViewCategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ViewCategoryAPIView(GenericAPIView):
    serializer_class= ViewCategorySerializer
    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self,request,pk):
        category= self.get_object(pk=pk)
        serializer= ViewCategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditCategoryAPIView(GenericAPIView):
    serializer_class= CategorySerializer
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        category= self.get_object(pk)
        serializer= CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        category= self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)