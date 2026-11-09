from django.db import models
from django.conf import settings


class Emergency(models.Model):

    EMERGENCY_TYPE_CHOICES = (
        ('SOS', 'SOS'),
        ('ACCIDENT', 'Accident'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('RESOLVED', 'Resolved'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergencies'
    )

    emergency_type = models.CharField(
        max_length=20,
        choices=EMERGENCY_TYPE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    ACCIDENT_TYPE_CHOICES = (
        ('ROAD_ACCIDENT', 'Road Accident'),
        ('VEHICLE_COLLISION', 'Vehicle Collision'),
        ('PEDESTRIAN', 'Pedestrian Accident'),
        ('WORKPLACE', 'Workplace Accident'),
        ('FIRE', 'Fire-related Accident'),
        ('OTHER', 'Other'),
    )

    REPORT_STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('VERIFIED', 'Verified'),
        ('REJECTED', 'Rejected'),
    )

    accident_type = models.CharField(
        max_length=30,
        choices=ACCIDENT_TYPE_CHOICES,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    accident_location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    accident_image = models.ImageField(
        upload_to='accident_reports/',
        blank=True,
        null=True
    )

    report_status = models.CharField(
        max_length=20,
        choices=REPORT_STATUS_CHOICES,
        default='SUBMITTED'
    )

    admin_remark = models.TextField(
        blank=True,
        null=True
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_accidents'
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.emergency_type} - {self.user.username}"

# Create your models here.
class EmergencyAlert(models.Model):

    ALERT_TYPE_CHOICES = (
        ('CONTACT', 'Emergency Contact'),
        ('HELPER', 'Helper'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('ACCEPTED', 'Accepted'),
    )

    emergency = models.ForeignKey(
        Emergency,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPE_CHOICES
    )

    recipient_email = models.EmailField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    location_shared = models.BooleanField(
        default=False
    )

    acceptance_token = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True
    )

    token_created_at = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.alert_type} - {self.status}"