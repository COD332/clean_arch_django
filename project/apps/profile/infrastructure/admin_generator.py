"""
Automatic admin configuration generator for entity-driven models
"""

from django.contrib import admin
from typing import Dict, List, Optional, Type
import dataclasses

class EntityAdminGenerator:
    """Generate Django admin configurations from entity dataclasses"""
    
    # Default field configurations
    DEFAULT_LIST_DISPLAY_FIELDS = ['id']
    DEFAULT_SEARCH_FIELDS = ['name']
    
    @classmethod
    def _get_readonly_fields(cls, model_class):
        """Get readonly fields that actually exist on the model"""
        model_field_names = [f.name for f in model_class._meta.fields]
        potential_readonly = ['created_at', 'updated_at', 'last_activity']
        return [field for field in potential_readonly if field in model_field_names]
    
    # Field type to filter mapping
    FILTER_FIELD_MAPPING = {
        'bool': 'list_filter',
        'datetime': 'list_filter',
        'choices': 'list_filter',
    }
    
    @classmethod
    def create_admin_class(cls, model_class, entity_class, 
                          custom_config: Optional[Dict] = None) -> Type[admin.ModelAdmin]:
        """Create an admin class for an entity-driven model"""
        
        if custom_config is None:
            custom_config = {}
        
        # Auto-generate admin configuration
        admin_config = cls._generate_admin_config(model_class, entity_class)
        
        # Apply custom overrides
        admin_config.update(custom_config)
        
        # Create admin class
        admin_class_name = f"{model_class.__name__}Admin"
        admin_class = type(admin_class_name, (admin.ModelAdmin,), admin_config)
        
        return admin_class
    
    @classmethod
    def _generate_admin_config(cls, model_class, entity_class) -> Dict:
        """Generate admin configuration from entity"""
        
        # Get model fields
        model_fields = [f.name for f in model_class._meta.fields]
        
        # Build list_display
        list_display = []
        list_filter = []
        search_fields = []
        
        # Analyze entity fields
        if dataclasses.is_dataclass(entity_class):
            entity_fields = {f.name: f.type for f in dataclasses.fields(entity_class)}
        else:
            entity_fields = {}
        
        for field_name in model_fields:
            field_obj = model_class._meta.get_field(field_name)
            
            # Add to list_display (exclude large text fields and foreign keys to User)
            if (field_name not in ['id'] and 
                not field_name.endswith('_ptr') and
                not (hasattr(field_obj, 'related_model') and 
                     field_obj.related_model and 
                     field_obj.related_model.__name__ == 'User' and 
                     field_name != 'user')):
                
                list_display.append(field_name)
            
            # Add to list_filter for appropriate field types
            if hasattr(field_obj, 'get_internal_type'):
                internal_type = field_obj.get_internal_type()
                if internal_type in ['BooleanField', 'DateTimeField', 'DateField']:
                    list_filter.append(field_name)
            
            # Add to search_fields for text fields
            if (hasattr(field_obj, 'get_internal_type') and 
                field_obj.get_internal_type() in ['CharField', 'TextField']):
                search_fields.append(field_name)
        
        # Add user-related search fields if user field exists
        if 'user' in model_fields:
            search_fields.extend(['user__username', 'user__email'])
        
        # Build fieldsets
        fieldsets = cls._build_fieldsets(model_fields)
        
        return {
            'list_display': tuple(list_display[:8]),  # Limit to reasonable number
            'list_filter': tuple(list_filter),
            'search_fields': tuple(search_fields),
            'readonly_fields': cls._get_readonly_fields(model_class),
            'fieldsets': fieldsets,
        }
    
    @classmethod
    def _build_fieldsets(cls, model_fields: List[str]) -> tuple:
        """Build fieldsets for admin form"""
        
        # Categorize fields
        main_fields = []
        relationship_fields = []
        timestamp_fields = []
        
        for field_name in model_fields:
            if field_name in ['created_at', 'updated_at', 'last_activity']:
                timestamp_fields.append(field_name)
            elif field_name in ['user', 'device'] or field_name.endswith('_id'):
                relationship_fields.append(field_name)
            elif field_name != 'id':
                main_fields.append(field_name)
        
        fieldsets = []
        
        # Main fields
        if main_fields:
            fieldsets.append((None, {'fields': tuple(main_fields)}))
        
        # Relationship fields
        if relationship_fields:
            fieldsets.append(('Relationships', {'fields': tuple(relationship_fields)}))
        
        # Timestamp fields
        if timestamp_fields:
            fieldsets.append(('Timestamps', {
                'fields': tuple(timestamp_fields),
                'classes': ('collapse',)
            }))
        
        return tuple(fieldsets)

def register_entity_admin(model_class, entity_class, custom_config: Optional[Dict] = None):
    """Decorator to register an entity-driven model with auto-generated admin"""
    
    admin_class = EntityAdminGenerator.create_admin_class(
        model_class, entity_class, custom_config
    )
    
    admin.site.register(model_class, admin_class)
    return admin_class
