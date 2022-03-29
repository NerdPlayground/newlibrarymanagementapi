from django.contrib import admin
from students.models import Student

# "id","user","first_name","last_name","registration_number","campus","faculty","course","mode_of_study"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display= [
        "id","user","first_name","last_name",
        "registration_number","campus",
        "faculty","course","mode_of_study"
    ]
    search_fields= ["first_name","last_name"]
    list_filter= ["campus","faculty","course","mode_of_study"]
    readonly_fields= [
        "user","first_name","last_name",
        "registration_number","campus",
        "faculty","course","mode_of_study"
    ]

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ["user","first_name","last_name"]
        return self.readonly_fields