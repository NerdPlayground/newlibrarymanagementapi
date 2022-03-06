import datetime
from fines.models import Fine
from django.http import Http404
from rest_framework import status
from students.models import Student
from fines.serializers import FineSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated

class UpdateFines:
    def difference(self,before):
        today,then= int(datetime.datetime.now().strftime("%d")),int(before.strftime("%d"))
        this_month,last_month= int(datetime.datetime.now().strftime("%m")),int(before.strftime("%m"))
        this_year,last_year= int(datetime.datetime.now().strftime("%Y")),int(before.strftime("%Y"))

        if int(this_year != last_year):
            days_till_end= int()
            days_till_now= int()
            days_of_months= [31,28,31,30,31,30,31,31,30,31,30,31]
            if last_year%4 == 0:
                days_of_months[1]= 29
            
            if last_month == 12:
                days_till_end= 31-then
            else:
                for days in range(last_month,12):
                    days_till_end += days_of_months[days]
                days_till_end += (last_month-then)
            
            if this_month == 1:
                days_till_now += today
            else:
                for days in range(0,this_month-1):
                    days_till_now += days_of_months[days]
                days_till_now += today
            
            return days_till_end+days_till_now

        elif int(this_month != last_month):
            last_month_days= (
                31 if last_month in [1,3,5,7,8,10,12]
                else 28 if last_month is 2 and last_year % 4 == 0
                else 30
            )
            return last_month_days+today-then

        else:
            return int(today)-int(then)
    
    def upddate_fine(self,fine):
        today= str(datetime.datetime.now()).replace(" ","T") + "Z"
        if fine.created_at is not today:
            fine.amount= self.difference(fine.transaction.issued_at)*50
            fine.save()

    def upddate_fines(self,fines):
        for fine in fines:
                self.upddate_fine(fine)

class FineAPIView(GenericAPIView):
    serializer_class= FineSerializer
    permission_classes= [IsAdminUser]
    def get(self,request):
        perform_update= UpdateFines()
        perform_update.upddate_fines(Fine.objects.all())
        fines= Fine.objects.all()
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class FineDetailAPIView(GenericAPIView):
    serializer_class= FineSerializer
    permission_classes= [IsAuthenticated]
    def get(self,request):
        student= Student.objects.get(user=request.user)
        perform_update= UpdateFines()
        perform_update.upddate_fines(Fine.objects.all())
        fines= Fine.objects.filter(student=student)
        serializer= FineSerializer(fines,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PayFineAPIView(GenericAPIView):
    permission_classes= [IsAuthenticated]
    def post(self,request):
        fine= Fine.objects.get(id=request.data.get('fine'))
        amount= request.data.get('amount')
        if amount < fine.amount:
            return Response({"Fine":fine.amount,"Message":"Please pay the full amount"},status=status.HTTP_200_OK)
        else:
            fine.delete()
            return Response({"Message":"Thank you for clearing your fine."},status=status.HTTP_200_OK)