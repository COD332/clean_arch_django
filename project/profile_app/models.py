from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Import models from the centralized registry
from .model_registry import Device, Session

# Re-export for convenience
__all__ = ['Device', 'Session']