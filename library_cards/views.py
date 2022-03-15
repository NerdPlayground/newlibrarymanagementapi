from django.http import Http404
from rest_framework import status
from students.models import Student
from library_cards.models import LibraryCard
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from library_cards.serializers import LibraryCardSerializer,LibraryCardStatusSerializer

class LibraryCardsAPIView(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class= LibraryCardSerializer

    def get(self,request):
        library_cards= LibraryCard.objects.all()
        serializer= LibraryCardSerializer(library_cards,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PatronLibraryCardAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class= LibraryCardSerializer

    def get(self,request):
        student= Student.objects.get(user=request.user)
        library_card= LibraryCard.objects.get(student=student)
        serializer= LibraryCardSerializer(library_card)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LibraryCardStatusAPIView(GenericAPIView):    
    permission_classes = [IsAdminUser]
    serializer_class= LibraryCardStatusSerializer

    def get_object(self,pk):
        try:
            return LibraryCard.objects.get(pk=pk)
        except LibraryCard.DoesNotExist:
            raise Http404

    def put(self,request,pk):
        library_card= self.get_object(pk)
        serializer= LibraryCardStatusSerializer(library_card,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)