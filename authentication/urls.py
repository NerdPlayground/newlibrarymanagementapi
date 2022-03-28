from django.urls import path
from authentication.views import (
    RegisterPatronAPIView,PatronsAPIView,
    PatronDetailAPIView,EditPatronAPIView,
    DeletePatronAPIView,DeleteAccountAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns= [
    path('register/',RegisterPatronAPIView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh-login/',TokenRefreshView.as_view(),name='login'),
    path('patrons/',PatronsAPIView.as_view(),name='patrons'),
    path('patron/',PatronDetailAPIView.as_view(),name='patron-detail'),
    path('edit-patron/<int:pk>/',EditPatronAPIView.as_view(),name='edit-patrons'),
    path('delete-account/',DeleteAccountAPIView.as_view(),name='delete'),
    path('delete-patron/<int:pk>/',DeletePatronAPIView.as_view(),name='delete-patron'),
]