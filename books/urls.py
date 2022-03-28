from django.urls import path
from books.views import AddBookAPIView,ViewBooksAPIView,ViewBookAPIView,EditBookAPIView

urlpatterns= [
    path('add-book/',AddBookAPIView.as_view(),name='add-book'),
    path('view-books/',ViewBooksAPIView.as_view(),name='view-books'),
    path('view-book/<str:pk>/',ViewBookAPIView.as_view(),name='view-book'),
    path('edit-book/<str:pk>/',EditBookAPIView.as_view(),name='edit-book'),
    path('delete-book/<str:pk>/',EditBookAPIView.as_view(),name='delete-book'),
]