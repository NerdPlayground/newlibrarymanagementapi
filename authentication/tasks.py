import random
from celery import shared_task
from students.models import Student
from django.contrib.auth.models import User

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

@shared_task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@shared_task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@shared_task(name="create_patron_object")
def patron():
    user = User.objects.create_user(
        first_name= "Bertilla",
        last_name= "Khavetsa",
        username= "reader_1803128",
        email= "bertilla@gmail.com"
    )
    user.set_password("bertilla23!@#")
    user.save()