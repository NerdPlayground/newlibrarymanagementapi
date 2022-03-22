from django.urls import path
from students.views import (
    UpdateAPIView,StudentAPIView,StudentDetailAPIView,
    CheckOutBookItemAPIView,ReturnBookItemAPIView,
    ModifyTransactionAPIView
)

urlpatterns= [
    path('student/update/',UpdateAPIView.as_view(),name='student-update'),
    path('students/',StudentAPIView.as_view(),name='students'),
    path('student/',StudentDetailAPIView.as_view(),name='student'),
    path('student/checkout-book-item/',CheckOutBookItemAPIView.as_view(),name='checkout-book-item'),
    path('student/return-book-item/',ReturnBookItemAPIView.as_view(),name='return-book-item'),
    path('modify/',ModifyTransactionAPIView.as_view(),name='modify-transaction')
]