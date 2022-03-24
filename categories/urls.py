from django.urls import path
from categories.views import (
    AddCategoryAPIView,ViewCategoriesAPIView,
    EditCategoriesAPIView,ViewCategoryAPIView
)

urlpatterns= [
    path('category/add/',AddCategoryAPIView.as_view(),name='add-category'),
    path('categories/view/',ViewCategoriesAPIView.as_view(),name='view-categories'),
    path('category/view/<str:pk>/',ViewCategoryAPIView.as_view(),name='view-category'),
    path('category/edit/<str:pk>/',EditCategoriesAPIView.as_view(),name='edit-category'),
]