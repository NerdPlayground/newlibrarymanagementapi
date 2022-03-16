from django.urls import path
from authors.views import AuthorAPIView,ViewAuthorAPIView,ViewAuthorsAPIView

urlpatterns= [
    path('authors/add/',AuthorAPIView.as_view(),name='add-authors'),
    path('authors/',ViewAuthorsAPIView.as_view(),name='all-authors'),
    path('authors/<int:pk>/',ViewAuthorAPIView.as_view(),name='individual-authors'),
]