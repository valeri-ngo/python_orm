from django.contrib import admin
from main_app.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'lecturer',
        'price',
        'start_date',
    )
    list_filter = (
        'is_published',
        'lecturer',
    )
    search_fields = (
        'title',
        'lecturer',
    )
    readonly_fields = (
        'start_date',
    )
    fieldsets = (
        (
            'Course Information', {
                'fields': (
                    'title',
                    'lecturer',
                    'price',
                    'start_date',
                    'is_published',
                )
            }
        ), (
            'Description', {
                'fields': (
                    'description',
                )
            }
        ),
    )
