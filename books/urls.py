from django.urls import path
from books.views import AddBookAPIView,ViewBooksAPIView,EditBooksAPIView

urlpatterns= [
    path('books/add/',AddBookAPIView.as_view(),name='add-books'),
    path('books/view/',ViewBooksAPIView.as_view(),name='view-books'),
    path('books/edit/<int:pk>/',EditBooksAPIView.as_view(),name='edit-books'),
]