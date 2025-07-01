from django.contrib import admin
from .model_registry import Device, Session
from .domain.entities import DeviceEntity, SessionEntity
from .infrastructure.admin_generator import register_entity_admin

# Auto-register Device with custom configuration
register_entity_admin(
    model_class=Device,
    entity_class=DeviceEntity,
    custom_config={
        'list_display': ('name', 'device_type', 'platform', 'user', 'is_active', 'created_at'),
        'list_filter': ('device_type', 'platform', 'is_active', 'created_at'),
        'search_fields': ('name', 'user__username', 'user__email'),
    }
)

# Auto-register Session with custom configuration
register_entity_admin(
    model_class=Session,
    entity_class=SessionEntity,
    custom_config={
        'list_display': ('session_token', 'user', 'device', 'ip_address', 'is_active', 'created_at', 'last_activity'),
        'list_filter': ('is_active', 'created_at', 'last_activity'),
        'search_fields': ('session_token', 'user__username', 'ip_address', 'user_agent'),
    }
)
