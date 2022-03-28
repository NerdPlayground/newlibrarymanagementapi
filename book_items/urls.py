from django.urls import path
from book_items.views import AddBookItemAPIView,BookItemsAPIView,BookItemDetailAPIView,EditBookItemAPIView

urlpatterns=[
    path('book-items/',BookItemsAPIView.as_view(),name='book-items'),
    path('add-book-item/',AddBookItemAPIView.as_view(),name='add-book-item'),
    path('view-book-item/<str:pk>/',BookItemDetailAPIView.as_view(),name='view-book-item'),
    path('update-book-item/<str:pk>/',EditBookItemAPIView.as_view(),name='update-book-item'),
    path('delete-book-item/<str:pk>/',EditBookItemAPIView.as_view(),name='delete-book-item'),
]