from django.urls import path
from categories.views import AddCategoryAPIView,ViewCategoriesAPIView,EditCategoriesAPIView

urlpatterns= [
    path('category/add/',AddCategoryAPIView.as_view(),name='add-category'),
    path('category/view/',ViewCategoriesAPIView.as_view(),name='view-category'),
    path('category/edit/<int:pk>/',EditCategoriesAPIView.as_view(),name='edit-category'),
]