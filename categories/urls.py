from django.urls import path
from categories.views import AddCategoryAPIView,ViewCategoriesAPIView,EditCategoriesAPIView

urlpatterns= [
    path('category/add/',AddCategoryAPIView.as_view(),name='add-category'),
    path('categories/view/',ViewCategoriesAPIView.as_view(),name='view-categories'),
    path('category/edit/<int:pk>/',EditCategoriesAPIView.as_view(),name='edit-category'),
]