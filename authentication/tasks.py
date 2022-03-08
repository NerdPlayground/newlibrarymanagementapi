import random
from celery import shared_task
from students.models import Student

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

@shared_task(name="get_student_object")
def get_student():
    student= Student.objects.get(pk=1)
    return {
        "student": student,
    }
