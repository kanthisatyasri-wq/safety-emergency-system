from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('SUPERADMIN', 'Super Admin'),
    ]
    

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )


    email_verified = models.BooleanField(default=False)

    otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    otp_created_at = models.DateTimeField(
        blank=True,
        null=True
    )
    otp_attempts = models.PositiveSmallIntegerField(default=0)

    # Aadhaar
    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )

    # Location
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

    location_type = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    location_address = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

# Create your models here.
