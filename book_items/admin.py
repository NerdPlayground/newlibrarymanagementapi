from django.contrib import admin
from book_items.models import BookItem

@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display= [
        "id","book","reference",
        "loaned_to","reserved_by","status",
        "purchased_on","published_on","rack"
    ]
    list_filter= ["book","reference","status"]
    readonly_fields= [
        "loaned_to","reserved_by",
        "status","published_on","rack"
    ]