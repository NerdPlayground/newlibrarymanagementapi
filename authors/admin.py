from books.models import Book
from django.contrib import admin
from authors.models import Author
from django.utils.html import format_html_join

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display= ["id","name","authored_books"]
    search_fields= ["name"]

    def authored_books(self,obj):
        books= Book.objects.filter(author=obj).values_list("name")
        return format_html_join(
            '\n',"<li>{}</li>",
            (book for book in books)
        )