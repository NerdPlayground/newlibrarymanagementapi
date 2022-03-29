from racks.models import Rack
from django.contrib import admin
from book_items.models import BookItem
from django.utils.html import format_html_join

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display= ["id","floor","segment","position","rack_number","books_contained"]
    list_filter= ["floor","segment","position"]

    def books_contained(self,obj):
        books= BookItem.objects.filter(rack=obj)
        if books:
            return books[0].book.name
    books_contained.short_description= "Books"