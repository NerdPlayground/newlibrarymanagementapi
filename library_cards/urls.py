from django.urls import path
from library_cards.views import LibraryCardsAPIView,PatronLibraryCardAPIView,LibraryCardStatusAPIView

urlpatterns= [
    path('library-cards/',LibraryCardsAPIView.as_view(),name='library-cards'),
    path('patron-library-card/',PatronLibraryCardAPIView.as_view(),name='patron-library-card'),
    path('library-card-status/<str:pk>/',LibraryCardStatusAPIView.as_view(),name='library-card-status'),
]