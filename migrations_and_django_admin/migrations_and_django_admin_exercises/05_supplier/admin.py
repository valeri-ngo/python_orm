from django.contrib import admin
from main_app.models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
    )
    list_filter = (
        'name',
        'phone',
    )
    search_fields = (
        'email',
        'contact_person',
        'phone',
    )
    list_per_page = 20
    fieldsets = (
        (
            'Information', {
                'fields': (
                    'name',
                    'contact_person',
                    'email',
                    'address',
                )
            }
        ),
    )
