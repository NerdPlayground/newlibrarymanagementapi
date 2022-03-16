from django.http import Http404
from rest_framework import status
from authors.models import Author
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView
from authors.serializers import AuthorSerializer,AuthorSerializer

class AuthorAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= [AuthorSerializer]
    def post(self,request):
        serializer= AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewAuthorsAPIView(GenericAPIView):
    serializer_class= [AuthorSerializer]
    def get(self,request):
        authors= Author.objects.all()
        serializer= AuthorSerializer(authors,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ViewAuthorAPIView(GenericAPIView):
    serializer_class= [AuthorSerializer]
    def get_object(self,pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        author= self.get_object(pk)
        serializer= AuthorSerializer(author)
        return Response(serializer.data,status=status.HTTP_200_OK)