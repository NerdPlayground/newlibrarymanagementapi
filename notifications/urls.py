from django.urls import path
from notifications.views import NotificationsAPIView,NotificationDetailAPIView

urlpatterns= [
    path('notifications/',NotificationsAPIView.as_view(),name='notifications'),
    path('notification/<str:pk>/',NotificationDetailAPIView.as_view(),name='notifications-detail'),
]