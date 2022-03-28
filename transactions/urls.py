from django.urls import path
from transactions.views import (
    LibraryTransactionsAPIView,
    TransactionDetailAPIView,
    PatronTransactionsAPIView
)

urlpatterns=[
    path('library-transactions/',LibraryTransactionsAPIView.as_view(),name='library-transactions'),
    path('patron-transactions/',PatronTransactionsAPIView.as_view(),name='patron-transactions'),
    path('patron-transaction/<str:pk>/',TransactionDetailAPIView.as_view(),name='patron-transaction'),
]