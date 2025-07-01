from typing import TypeVar, Type, List
from django.db import models
from datetime import datetime

EntityType = TypeVar('EntityType')
ModelType = TypeVar('ModelType', bound=models.Model)

class EntityModelMapper:
    """Handles conversion between entities and Django models"""
    
    @staticmethod
    def entity_to_model_data(entity, exclude_fields=None):
        """Convert entity to dictionary suitable for Django model creation/update"""
        if exclude_fields is None:
            exclude_fields = {'device_id', 'username'}  # Fields that shouldn't be in model data
        
        entity_dict = {}
        for field_name in dir(entity):
            if (not field_name.startswith('_') and 
                field_name not in exclude_fields and
                not callable(getattr(entity, field_name))):
                
                value = getattr(entity, field_name)
                if value is not None:
                    entity_dict[field_name] = value
        
        return entity_dict
    
    @staticmethod
    def model_to_entity(model_instance, entity_class: Type[EntityType], field_mapping=None) -> EntityType:
        """Convert Django model instance to entity"""
        if field_mapping is None:
            field_mapping = {}
        
        # Get entity field names from the dataclass
        import dataclasses
        if dataclasses.is_dataclass(entity_class):
            entity_fields = {f.name for f in dataclasses.fields(entity_class)}
        else:
            # Fallback: get from __init__ signature
            import inspect
            entity_fields = set(inspect.signature(entity_class.__init__).parameters.keys())
            entity_fields.discard('self')
        
        entity_data = {}
        
        for field_name in entity_fields:
            # Use field mapping if provided
            model_field_name = field_mapping.get(field_name, field_name)
            
            # Special handling for specific fields
            if field_name == 'device_id':
                entity_data[field_name] = model_instance.id
            elif field_name == 'username' and hasattr(model_instance, 'user'):
                entity_data[field_name] = model_instance.user.username
            elif hasattr(model_instance, model_field_name):
                entity_data[field_name] = getattr(model_instance, model_field_name)
        
        return entity_class(**entity_data)
    
    @staticmethod
    def models_to_entities(model_instances: List[ModelType], entity_class: Type[EntityType], 
                          field_mapping=None) -> List[EntityType]:
        """Convert list of Django model instances to list of entities"""
        return [
            EntityModelMapper.model_to_entity(instance, entity_class, field_mapping)
            for instance in model_instances
        ]
