from django.contrib import admin
from .models import Emergency
from .models import EmergencyAlert


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'emergency_type',
        'status',
        'latitude',
        'longitude',
        'created_at',
    )

    list_filter = (
        'emergency_type',
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
    )
@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'emergency',
        'alert_type',
        'recipient_email',
        'status',
        'location_shared',
        'created_at',
    )

    list_filter = (
        'alert_type',
        'status',
        'location_shared',
    )

    search_fields = (
        'recipient_email',
    )
# Register your models here.
