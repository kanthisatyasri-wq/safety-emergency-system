from django.contrib import admin
from django.contrib import admin

from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'contact_type',
        'name',
        'email',
        'phone',
        'created_at',
    )

    list_filter = (
        'contact_type',
        'created_at',
    )

    search_fields = (
        'user__username',
        'name',
        'email',
        'phone',
    )


# Register your models here.
