from books.models import Book
from django.contrib import admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display= [
        "id","isbn","category","name",
        "description","published_on",
        "publisher","language","pages"
    ]
    list_filter= ["category","publisher","language"]
    search_fields= ["name"]