from django.urls import path
from categories.views import (
    AddCategoryAPIView,ViewCategoriesAPIView,
    EditCategoryAPIView,ViewCategoryAPIView
)

urlpatterns= [
    path('add-category/',AddCategoryAPIView.as_view(),name='add-category'),
    path('view-categories/',ViewCategoriesAPIView.as_view(),name='view-categories'),
    path('view-category/<str:pk>/',ViewCategoryAPIView.as_view(),name='view-category'),
    path('edit-category/<str:pk>/',EditCategoryAPIView.as_view(),name='edit-category'),
    path('delete-category/<str:pk>/',EditCategoryAPIView.as_view(),name='delete-category'),
]