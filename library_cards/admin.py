from django.contrib import admin
from library_cards.models import LibraryCard

@admin.register(LibraryCard)
class LibraryCardAdmin(admin.ModelAdmin):
    list_display= ["id","student","issued_at","active"]
    list_filter= ["active"]
    readonly_fields= ["student","issued_at"]