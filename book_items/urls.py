from django.urls import path
from book_items.views import BookItemAPIView,BookItemDetailAPIView

urlpatterns=[
    path('book-items/',BookItemAPIView.as_view(),name='book-items'),
    path('book-items/add/',BookItemAPIView.as_view(),name='add-book-items'),
    path('book-items/view/<int:pk>/',BookItemDetailAPIView.as_view(),name='view-book-item'),
    path('book-items/update/<int:pk>/',BookItemDetailAPIView.as_view(),name='update-book-items'),
]