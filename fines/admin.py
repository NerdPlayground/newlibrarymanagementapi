from fines.models import Fine
from django.contrib import admin

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display= ["id","created_at","transaction","amount","paid_on"]
    readonly_fields= ["created_at","transaction","amount","paid_on"]