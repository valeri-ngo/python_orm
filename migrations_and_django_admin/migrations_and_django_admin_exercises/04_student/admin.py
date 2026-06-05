from django.contrib import admin
from main_app.models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'age',
        'grade',
    )
    list_filter = (
        'age',
        'grade',
        'date_of_birth',
    )
    search_fields = (
        'first_name',
    )
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'age',
                'date_of_birth'
            )
        }),
        ('Academic Information', {
            'fields': (
                'grade',
            )
        }),
    )
