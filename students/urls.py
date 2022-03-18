from django.urls import path
from students.views import UpdateAPIView,StudentAPIView,StudentDetailAPIView,CheckOutBookItemAPIView

urlpatterns= [
    path('student/update/',UpdateAPIView.as_view(),name='student-update'),
    path('students/',StudentAPIView.as_view(),name='students'),
    path('student/',StudentDetailAPIView.as_view(),name='student'),
    path('student/checkout-book-item/',CheckOutBookItemAPIView.as_view(),name='checkout-book-item')
]