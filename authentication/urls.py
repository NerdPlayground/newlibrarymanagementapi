from django.urls import path
from authentication.views import (
    RegisterAPIView,LoginAPIView,UserAPIView,
    DeleteAPIView,UserDetailAPIView,EditUserAPIView
)

urlpatterns= [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('users/',UserAPIView.as_view(),name='users'),
    path('user/',UserDetailAPIView.as_view(),name='user-detail'),
    path('users/<int:pk>/',EditUserAPIView.as_view(),name='edit-users'),
    path('delete/',DeleteAPIView.as_view(),name='delete'),
]