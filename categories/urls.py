from django.urls import path
from categories.views import AddCategoryAPIView,ViewCategoriesAPIView,EditCategoriesAPIView,ViewCategoryAPIView

urlpatterns= [
    path('category/add/',AddCategoryAPIView.as_view(),name='add-category'),
    path('categories/view/',ViewCategoriesAPIView.as_view(),name='view-categories'),
    path('category/view/<int:pk>/',ViewCategoryAPIView.as_view(),name='view-category'),
    path('category/edit/<int:pk>/',EditCategoriesAPIView.as_view(),name='edit-category'),
]