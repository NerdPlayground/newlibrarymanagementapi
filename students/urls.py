from django.urls import path
from students.views import (
    UpdateAPIView,StudentsAPIView,
    StudentDetailAPIView,CheckOutBookItemAPIView,
    ReturnBookItemAPIView,RenewBookItemAPIView
)

urlpatterns= [
    path('update-student/',UpdateAPIView.as_view(),name='student-update'),
    path('students/',StudentsAPIView.as_view(),name='students'),
    path('student/',StudentDetailAPIView.as_view(),name='student'),
    path('checkout-book-item/',CheckOutBookItemAPIView.as_view(),name='checkout-book-item'),
    path('return-book-item/',ReturnBookItemAPIView.as_view(),name='return-book-item'),
    path('renew-book-item/',RenewBookItemAPIView.as_view(),name='renew-book-item'),
]