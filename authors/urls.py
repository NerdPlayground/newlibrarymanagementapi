from django.urls import path
from authors.views import AuthorAPIView,AuthorsAPIView,AuthorDetailAPIView

urlpatterns= [
    path('authors/add/',AuthorAPIView.as_view(),name='add-author'),
    path('authors/',AuthorsAPIView.as_view(),name='all-authors'),
    path('author/<str:pk>/',AuthorDetailAPIView.as_view(),name='individual-author'),
]