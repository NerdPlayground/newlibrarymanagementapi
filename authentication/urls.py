from django.urls import path
from authentication.views import (
    RegisterAPIView,UserAPIView,
    DeleteAPIView,UserDetailAPIView,EditUserAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns= [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('login/refresh/',TokenRefreshView.as_view(),name='login'),
    path('users/',UserAPIView.as_view(),name='users'),
    path('user/',UserDetailAPIView.as_view(),name='user-detail'),
    path('users/<int:pk>/',EditUserAPIView.as_view(),name='edit-users'),
    path('delete/',DeleteAPIView.as_view(),name='delete'),
]