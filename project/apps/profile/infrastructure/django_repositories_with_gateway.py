"""
Django repository implementations using the DTO/Gateway pattern.
These repositories use gateways to convert between entities and Django models.
"""

from typing import List, Optional
from django.contrib.auth.models import User

from ..domain.entities import UserEntity, DeviceEntity, SessionEntity
from ..domain.repositories import UserRepository, DeviceRepository, SessionRepository
from ..models import Device, Session
from .gateways import UserGateway, DeviceGateway, SessionGateway


class DjangoUserRepositoryWithGateway(UserRepository):
    """User repository implementation using DTO/Gateway pattern"""

    def add(self, user: UserEntity) -> UserEntity:
        """Add a new user"""
        dto = UserGateway.entity_to_dto(user)
        django_user = UserGateway.dto_to_model(dto)
        
        if user.password:
            django_user.set_password(user.password)
        
        django_user.save()
        
        return UserGateway.model_to_entity(django_user)

    def find_by_username(self, username: str) -> Optional[UserEntity]:
        """Find user by username"""
        try:
            django_user = User.objects.get(username=username)
            return UserGateway.model_to_entity(django_user)
        except User.DoesNotExist:
            return None

    def delete(self, username: str) -> None:
        """Delete user by username"""
        User.objects.filter(username=username).delete()

    def change_password(self, username: str, new_password: str) -> None:
        """Change user password"""
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()


class DjangoDeviceRepositoryWithGateway(DeviceRepository):
    """Device repository implementation using DTO/Gateway pattern"""

    def add(self, device: DeviceEntity) -> DeviceEntity:
        """Add a new device"""
        # Get user for the device
        user = User.objects.get(username=device.username)
        
        dto = DeviceGateway.entity_to_dto(device, user.id)
        django_device = DeviceGateway.dto_to_model(dto)
        django_device.save()
        
        return DeviceGateway.model_to_entity(django_device)

    def find_by_name_and_user(self, name: str, username: str) -> Optional[DeviceEntity]:
        """Find device by name and user"""
        try:
            django_device = Device.objects.get(name=name, user__username=username)
            return DeviceGateway.model_to_entity(django_device)
        except Device.DoesNotExist:
            return None

    def find_by_id(self, device_id: int) -> Optional[DeviceEntity]:
        """Find device by ID"""
        try:
            django_device = Device.objects.get(id=device_id)
            return DeviceGateway.model_to_entity(django_device)
        except Device.DoesNotExist:
            return None

    def find_by_user(self, username: str) -> List[DeviceEntity]:
        """Find all devices for a user"""
        devices = Device.objects.filter(user__username=username)
        return [DeviceGateway.model_to_entity(device) for device in devices]

    def update(self, device: DeviceEntity) -> DeviceEntity:
        """Update an existing device"""
        # Get user for the device
        user = User.objects.get(username=device.username)
        
        dto = DeviceGateway.entity_to_dto(device, user.id)
        django_device = DeviceGateway.dto_to_model(dto)
        django_device.save()
        
        return DeviceGateway.model_to_entity(django_device)

    def delete(self, device_id: int) -> None:
        """Delete device by ID"""
        Device.objects.filter(id=device_id).delete()

    def delete_by_name_and_user(self, name: str, username: str) -> None:
        """Delete device by name and user"""
        Device.objects.filter(name=name, user__username=username).delete()

    def delete_by_id(self, device_id: int) -> None:
        """Delete device by ID"""
        Device.objects.filter(id=device_id).delete()

    def set_active_status(self, name: str, username: str, is_active: bool) -> None:
        """Set device active status"""
        device = Device.objects.get(name=name, user__username=username)
        device.is_active = is_active
        device.save()


class DjangoSessionRepositoryWithGateway(SessionRepository):
    """Session repository implementation using DTO/Gateway pattern"""

    def add(self, session: SessionEntity) -> SessionEntity:
        """Add a new session"""
        # Get user for the session
        user = User.objects.get(username=session.username)
        
        # Get device if specified
        device_id = None
        if session.device_name:
            try:
                device = Device.objects.get(name=session.device_name, user=user)
                device_id = device.id
            except Device.DoesNotExist:
                pass
        
        dto = SessionGateway.entity_to_dto(session, user.id, device_id)
        django_session = SessionGateway.dto_to_model(dto)
        django_session.save()
        
        return SessionGateway.model_to_entity(django_session)

    def find_by_token(self, token: str) -> Optional[SessionEntity]:
        """Find session by token"""
        try:
            django_session = Session.objects.get(session_token=token)
            return SessionGateway.model_to_entity(django_session)
        except Session.DoesNotExist:
            return None

    def find_by_user(self, username: str) -> List[SessionEntity]:
        """Find all sessions for a user"""
        sessions = Session.objects.filter(user__username=username)
        return [SessionGateway.model_to_entity(session) for session in sessions]

    def find_active_by_user(self, username: str) -> List[SessionEntity]:
        """Find all active sessions for a user"""
        sessions = Session.objects.filter(user__username=username, is_active=True)
        return [SessionGateway.model_to_entity(session) for session in sessions]

    def update_last_activity(self, token: str) -> None:
        """Update session last activity"""
        from django.utils import timezone
        Session.objects.filter(session_token=token).update(last_activity=timezone.now())

    def deactivate(self, token: str) -> None:
        """Deactivate session"""
        Session.objects.filter(session_token=token).update(is_active=False)

    def deactivate_user_sessions(self, username: str) -> None:
        """Deactivate all sessions for a user"""
        Session.objects.filter(user__username=username).update(is_active=False)

    def delete(self, token: str) -> None:
        """Delete session by token"""
        Session.objects.filter(session_token=token).delete()

    def delete_inactive_sessions(self) -> None:
        """Delete all inactive sessions"""
        Session.objects.filter(is_active=False).delete()
