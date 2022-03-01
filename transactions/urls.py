from django.urls import path
from transactions.views import TransactionAPIView,TransactionDetailAPIView

urlpatterns=[
    path('transactions/',TransactionAPIView.as_view(),name='user-transactions'),
    path('transactions/user/',TransactionDetailAPIView.as_view(),name='user-transactions')
]