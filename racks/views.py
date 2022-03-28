from racks.models import Rack
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from racks.serializers import AddRackSerializer,ViewRackSerializer

class AddRackAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= AddRackSerializer

    def post(self,request):
        serializer= AddRackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewRacksAPIView(GenericAPIView):
    serializer_class= ViewRackSerializer

    def get(self,request):
        racks= Rack.objects.all()
        serializer= ViewRackSerializer(racks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)