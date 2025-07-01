from django.contrib import admin
from .models import Device, Session


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'platform', 'user', 'is_active', 'created_at')
    list_filter = ('device_type', 'platform', 'is_active', 'created_at')
    search_fields = ('name', 'user__username', 'user__email')
    list_select_related = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Device Information', {
            'fields': ('name', 'device_type', 'platform', 'user', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_token_short', 'user', 'device', 'ip_address', 'is_active', 'created_at', 'last_activity')
    list_filter = ('is_active', 'created_at', 'last_activity')
    search_fields = ('session_token', 'user__username', 'ip_address', 'user_agent')
    list_select_related = ('user', 'device')
    readonly_fields = ('created_at', 'last_activity')
    
    fieldsets = (
        ('Session Information', {
            'fields': ('session_token', 'user', 'device', 'is_active')
        }),
        ('Client Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_activity'),
            'classes': ('collapse',)
        }),
    )
    
    def session_token_short(self, obj):
        return f"{obj.session_token[:10]}..."
    session_token_short.short_description = 'Session Token'
