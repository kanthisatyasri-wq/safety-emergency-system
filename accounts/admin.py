from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'email_verified',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'email_verified',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Safety System Information', {
            'fields': (
                'role',
                'email_verified',
                'aadhaar_number',
                'latitude',
                'longitude',
                'location_type',
                'location_address',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Safety System Information', {
            'fields': (
                'email',
                'role',
                'aadhaar_number',
            )
        }),
    )