from django.urls import path
from authors.views import (
    AuthorAPIView,AuthorsAPIView,
    AuthorDetailAPIView,DeleteAuthorAPIView
)

urlpatterns= [
    path('add-author/',AuthorAPIView.as_view(),name='add-author'),
    path('authors/',AuthorsAPIView.as_view(),name='all-authors'),
    path('author/<str:pk>/',AuthorDetailAPIView.as_view(),name='individual-author'),
    path('delete-author/<str:pk>/',DeleteAuthorAPIView.as_view(),name='delete-author'),
]