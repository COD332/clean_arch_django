"""
Django models for the profile app.
These models are separate from domain entities and are designed for database persistence.
"""

from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    """Django model for Device persistence"""
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'device'
        unique_together = ('name', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Session(models.Model):
    """Django model for Session persistence"""
    session_token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'session'
        ordering = ['-last_activity']

    def __str__(self):
        return f"Session for {self.user.username} - {self.session_token[:10]}..."