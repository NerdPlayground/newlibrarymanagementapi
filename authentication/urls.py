from django.urls import path
from authentication.views import RegisterAPIView,LoginAPIView,UserAPIView,DeleteAPIView

urlpatterns= [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('users/',UserAPIView.as_view(),name='users'),
    path('user/delete/<int:pk>/',DeleteAPIView.as_view(),name='delete'),
]