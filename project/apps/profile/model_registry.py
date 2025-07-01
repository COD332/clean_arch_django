"""
Centralized registry for entity-driven models
This ensures all parts of the application use the same dynamically generated models
"""

from django.db import models
from django.contrib.auth.models import User
from .domain.entities import DeviceEntity, SessionEntity
from .infrastructure.model_generator import create_model_from_entity

class ModelRegistry:
    """Registry for all entity-driven models"""
    
    _models = {}
    
    @classmethod
    def register_model(cls, entity_class, model_name, additional_fields=None, meta_options=None):
        """Register a new model generated from an entity"""
        if model_name in cls._models:
            return cls._models[model_name]
        
        model_class = create_model_from_entity(
            entity_class=entity_class,
            model_name=model_name,
            additional_fields=additional_fields,
            meta_options=meta_options
        )
        
        cls._models[model_name] = model_class
        return model_class
    
    @classmethod
    def get_model(cls, model_name):
        """Get a registered model by name"""
        if model_name not in cls._models:
            raise ValueError(f"Model '{model_name}' is not registered")
        return cls._models[model_name]
    
    @classmethod
    def get_all_models(cls):
        """Get all registered models"""
        return cls._models.copy()

# Register all models
Device = ModelRegistry.register_model(
    entity_class=DeviceEntity,
    model_name='Device',
    additional_fields={
        'user': models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices'),
    },
    meta_options={
        'unique_together': ('name', 'user'),
    }
)

Session = ModelRegistry.register_model(
    entity_class=SessionEntity,
    model_name='Session',
    additional_fields={
        'user': models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions'),
        'device': models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions'),
    },
    meta_options={
        'ordering': ['-last_activity'],
    }
)

# Export models for easy import
__all__ = ['Device', 'Session', 'ModelRegistry']
