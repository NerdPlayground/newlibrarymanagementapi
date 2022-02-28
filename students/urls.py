from django.urls import path
from students.views import UpdateAPIView,StudentAPIView,StudentDetailAPIView

urlpatterns= [
    path('student/update/',UpdateAPIView.as_view(),name='student-update'),
    path('students/',StudentAPIView.as_view(),name='students'),
    path('student/',StudentDetailAPIView.as_view(),name='student'),
]