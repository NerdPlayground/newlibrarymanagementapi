from django.contrib import admin
from transactions.models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display= ["id","student","book_item","issued_at","overdue","due_date","returned","returned_at"]
    readonly_fields= ["student","book_item","issued_at","overdue","due_date","returned","returned_at"]