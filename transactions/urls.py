from django.urls import path
from transactions.views import (
    LibraryTransactionsAPIView,
    TransactionDetailAPIView,
    PatronTransactionsAPIView
)

urlpatterns=[
    path('transactions/',LibraryTransactionsAPIView.as_view(),name='user-transactions'),
    path('transactions/user/',PatronTransactionsAPIView.as_view(),name='user-transactions'),
    path('transactions/user/<str:pk>/',TransactionDetailAPIView.as_view(),name='user-transaction'),
]