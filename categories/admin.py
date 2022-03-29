from books.models import Book
from django.contrib import admin
from categories.models import Category
from django.utils.html import format_html_join

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ["id","name","description","category_books"]
    search_fields= ["name"]

    def category_books(self,obj):
        books= Book.objects.filter(category=obj).values_list("name")
        return format_html_join(
            '\n',"<li>{}</li>",
            (book for book in books)
        )