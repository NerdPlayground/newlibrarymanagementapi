from django.urls import path
from authentication.views import RegisterAPIView,LoginAPIView,UserAPIView

urlpatterns= [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('users/',UserAPIView.as_view(),name='users'),
]