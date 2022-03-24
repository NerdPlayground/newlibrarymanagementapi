from django.urls import path
from books.views import AddBookAPIView,ViewBooksAPIView,EditBookAPIView,ViewBookAPIView

urlpatterns= [
    path('book/add/',AddBookAPIView.as_view(),name='add-books'),
    path('books/view/',ViewBooksAPIView.as_view(),name='view-books'),
    path('book/view/<str:pk>/',ViewBookAPIView.as_view(),name='view-book'),
    path('book/edit/<str:pk>/',EditBookAPIView.as_view(),name='edit-books'),
]