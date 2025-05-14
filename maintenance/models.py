from django.db import models
from django.utils import timezone
from django.conf import settings

class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.service_type})"

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    tenant = models.ForeignKey('core.TenantProfile', on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE, related_name='maintenance_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    damage_photo = models.ImageField(upload_to='maintenance_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class MaintenanceLog(models.Model):
    STATUS_CHOICES = MaintenanceRequest.STATUS_CHOICES

    maintenance_request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='logs')
    note = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Log for {self.maintenance_request.title} by {self.updated_by}"



