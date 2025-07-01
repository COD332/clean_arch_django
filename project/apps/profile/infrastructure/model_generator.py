from django.db import models
from django.contrib.auth.models import User
from typing import get_type_hints, get_origin, get_args, Optional, Union
from datetime import datetime
import dataclasses

class EntityToModelConverter:
    """Converts entity dataclasses to Django models"""
    
    # Mapping from Python types to Django field types
    TYPE_MAPPING = {
        str: {'field_class': models.CharField, 'default_kwargs': {'max_length': 255}},
        int: {'field_class': models.IntegerField, 'default_kwargs': {}},
        bool: {'field_class': models.BooleanField, 'default_kwargs': {'default': False}},
        datetime: {'field_class': models.DateTimeField, 'default_kwargs': {}},
    }
    
    # Special field handling
    SPECIAL_FIELDS = {
        'created_at': lambda: models.DateTimeField(auto_now_add=True),
        'updated_at': lambda: models.DateTimeField(auto_now=True),
        'is_active': lambda: models.BooleanField(default=True),
    }
    
    # Fields to exclude from Django model (handled differently)
    EXCLUDED_FIELDS = {'device_id', 'username'}
    
    @classmethod
    def convert_entity_to_model(cls, entity_class, model_name, additional_fields=None, meta_options=None):
        """Convert an entity dataclass to a Django model"""
        
        if not dataclasses.is_dataclass(entity_class):
            raise ValueError(f"{entity_class} is not a dataclass")
        
        # Get type hints from the entity
        type_hints = get_type_hints(entity_class)
        
        # Generate Django model fields
        model_fields = {}
        
        for field_name, field_type in type_hints.items():
            # Skip excluded fields
            if field_name in cls.EXCLUDED_FIELDS:
                continue
            
            # Handle special fields
            if field_name in cls.SPECIAL_FIELDS:
                model_fields[field_name] = cls.SPECIAL_FIELDS[field_name]()
                continue
            
            # Handle Optional types (Union[Type, None])
            is_optional = False
            if get_origin(field_type) is Union:
                args = get_args(field_type)
                if len(args) == 2 and type(None) in args:
                    field_type = args[0] if args[1] is type(None) else args[1]
                    is_optional = True
            
            # Get Django field for this type
            django_field = cls._get_django_field(field_name, field_type, is_optional)
            if django_field:
                model_fields[field_name] = django_field
        
        # Add additional fields if provided
        if additional_fields:
            model_fields.update(additional_fields)
        
        # Create Meta class
        meta_attrs = {'db_table': model_name.lower()}
        if meta_options:
            meta_attrs.update(meta_options)
        Meta = type('Meta', (), meta_attrs)
        
        # Create model attributes
        model_attrs = {
            **model_fields,
            'Meta': Meta,
            '__module__': 'apps.profile.models',
            '__str__': cls._create_str_method(model_name),
        }
        
        # Create and return the model class
        return type(model_name, (models.Model,), model_attrs)
    
    @classmethod
    def _get_django_field(cls, field_name, field_type, is_optional):
        """Get appropriate Django field for a given Python type"""
        
        if field_type not in cls.TYPE_MAPPING:
            # Default to CharField for unknown types
            return models.CharField(max_length=255, null=is_optional, blank=is_optional)
        
        field_info = cls.TYPE_MAPPING[field_type]
        field_class = field_info['field_class']
        kwargs = field_info['default_kwargs'].copy()
        
        # Add null/blank for optional fields
        if is_optional:
            kwargs['null'] = True
            kwargs['blank'] = True
        
        # Special handling for specific field names
        if field_name in ['name', 'device_type', 'platform'] and field_type == str:
            kwargs['max_length'] = 255
        elif field_type == str and 'max_length' not in kwargs:
            kwargs['max_length'] = 100
        
        return field_class(**kwargs)
    
    @classmethod
    def _create_str_method(cls, model_name):
        """Create a __str__ method for the model"""
        def __str__(self):
            if hasattr(self, 'name') and hasattr(self, 'user'):
                return f"{self.name} - {self.user.username}"
            elif hasattr(self, 'name'):
                return self.name
            else:
                return f"{model_name} {self.id}"
        return __str__

# Convenience function
def create_model_from_entity(entity_class, model_name, additional_fields=None, meta_options=None):
    """Create a Django model from an entity dataclass"""
    return EntityToModelConverter.convert_entity_to_model(
        entity_class, model_name, additional_fields, meta_options
    )
