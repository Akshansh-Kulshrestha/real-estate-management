from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('identity', 'Identity Document'),
        ('ownership', 'Ownership Proof'),
        ('lease', 'Lease Agreement'),
        ('other', 'Other')
    ]

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.document_type} by {self.uploaded_by.username}"


class Verification(models.Model):
    VERIFICATION_TYPES = [
        ('user', 'User Verification'),
        ('property', 'Property Verification')
    ]

    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPES)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    target_property = models.ForeignKey('core.Property', on_delete=models.CASCADE, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        if self.verification_type == 'user':
            return f"User Verification - {self.target_user.username}"
        elif self.verification_type == 'property':
            return f"Property Verification - {self.target_property}"
        return "Verification"