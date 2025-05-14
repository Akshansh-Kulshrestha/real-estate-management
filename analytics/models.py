from django.db import models
from django.utils import timezone

class PropertyView(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} viewed {self.property} at {self.viewed_at}"

class SearchQuery(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    query_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched '{self.query_text}'"

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('property', 'Property'),
        ('platform', 'Platform'),
    ]

    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_TYPE_CHOICES)
    property = models.ForeignKey('core.Property', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type} feedback from {self.user}"

