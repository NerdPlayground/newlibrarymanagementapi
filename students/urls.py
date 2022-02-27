from django.urls import path
from students.views import UpdateAPIView,StudentAPIView

urlpatterns= [
    path('student/update/',UpdateAPIView.as_view(),name='student-update'),
    path('students/',StudentAPIView.as_view(),name='students')
]