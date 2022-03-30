import datetime
from django.http import Http404
from rest_framework import status
from students.models import Student
from django.contrib.auth.models import User
from rest_framework.response import Response
from library_cards.models import LibraryCard
from rest_framework.generics import GenericAPIView
from library_cards.card_status import verify_patron
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from authentication.serializers import RegisterPatronSerializer,PatronSerializer,EditPatronSerializer

class RegisterPatronAPIView(GenericAPIView):
    serializer_class= RegisterPatronSerializer
    def post(self,request):
        serializer= RegisterPatronSerializer(data=request.data)
        if serializer.is_valid():
            first_name= request.data.get('first_name')
            last_name= request.data.get('last_name')
            registration_number= request.data.get('registration_number')
            username= "reader_"+registration_number[:2]+registration_number[3:]
            email= request.data.get('email')
            password= request.data.get('password')

            user = User.objects.create_user(
                first_name= first_name,
                last_name= last_name,
                username= username,
                email= email,
            )
            user.set_password(password)
            user.save()
            
            student= Student.objects.create(
                user= user,
                first_name= user.first_name,
                last_name= user.last_name,
                registration_number= registration_number
            )
            student.save()

            library_card= LibraryCard.objects.create(
                student= student,
                issued_at= datetime.date.today(),
                active= True
            )
            library_card.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatronsAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]
    serializer_class= PatronSerializer

    def get(self,request):
        users= User.objects.all()
        serializer= PatronSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PatronDetailAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= PatronSerializer

    def get(self,request):
        if verify_patron(request=request):
            user= request.user
            serializer= PatronSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"Library card has been revoked"},status=status.HTTP_400_BAD_REQUEST)

class EditPatronAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= EditPatronSerializer

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def put(self,request,pk):
        if not request.user.is_staff:
            if verify_patron(request=request):
                user= self.get_object(pk)
                serializer= EditPatronSerializer(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"Warning":"Administrator access denied."},
                status=status.HTTP_400_BAD_REQUEST
            )

class DeleteAccountAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]

    def delete(self,request):
        if verify_patron(request=request):
            user= request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                    {"message":"Library card has been revoked"},
                    status=status.HTTP_400_BAD_REQUEST
            )

class DeletePatronAPIView(GenericAPIView):
    permission_classes= [IsAdminUser]

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def delete(self,request,pk):
        user= self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)