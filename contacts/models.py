from django.db import models
from django.conf import settings


class EmergencyContact(models.Model):

    CONTACT_TYPE_CHOICES = (
        ('FATHER', 'Father'),
        ('MOTHER', 'Mother'),
        ('BROTHER', 'Brother'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='emergency_contacts'
    )

    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPE_CHOICES
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    # Email verification
    email_verified = models.BooleanField(
        default=False
    )

    verification_otp = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    otp_created_at = models.DateTimeField(
        blank=True,
        null=True
    )
    

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    otp_attempts = models.PositiveSmallIntegerField(default=0)
    

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'contact_type'],
                name='unique_contact_type_per_user'
            )
        ]

    def __str__(self):
        return f"{self.contact_type} - {self.name}"

