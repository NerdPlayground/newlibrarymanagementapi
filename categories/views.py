from rest_framework import status
from categories.models import Category
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser
from categories.serializers import CategorySerializer

class AddCategoryAPIView(APIView):
    def post(serlf,request):
        serializer= CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewCategoriesAPIView(APIView):
    def get(self,request):
        categories= Category.objects.all()
        serializer= CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditCategoriesAPIView(APIView):
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