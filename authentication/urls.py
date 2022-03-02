from django.urls import path
from authentication.views import (
    RegisterAPIView,LoginAPIView,UserAPIView,
    RequestBookAPIView,IssueBookAPIView,
    DeleteAPIView,DeleteDetailAPIView
)

urlpatterns= [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('users/',UserAPIView.as_view(),name='users'),
    path('request-book/',RequestBookAPIView.as_view(),name='request-book'),
    path('issue-book/<int:pk>/',IssueBookAPIView.as_view(),name='issue-book'),
    path('delete/',DeleteAPIView.as_view(),name='delete'),
    path('delete/<int:pk>/',DeleteDetailAPIView.as_view(),name='user-delete'),
]