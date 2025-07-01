"""
Example service implementations using the new DTO/Gateway pattern.
These services show how to use the gateways for data conversion between layers.
"""

from typing import List, Optional
from ..domain.entities import UserEntity, DeviceEntity, SessionEntity
from ..infrastructure.django_repositories_with_gateway import (
    DjangoUserRepositoryWithGateway,
    DjangoDeviceRepositoryWithGateway,
    DjangoSessionRepositoryWithGateway
)


class UserServiceWithGateway:
    """User service using DTO/Gateway pattern"""

    def __init__(self):
        self.user_repository = DjangoUserRepositoryWithGateway()

    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        """Create a new user"""
        user_entity = UserEntity(
            username=username,
            email=email,
            password=password
        )
        return self.user_repository.add(user_entity)

    def get_user(self, username: str) -> Optional[UserEntity]:
        """Get user by username"""
        return self.user_repository.find_by_username(username)

    def update_password(self, username: str, new_password: str) -> None:
        """Update user password"""
        self.user_repository.change_password(username, new_password)

    def delete_user(self, username: str) -> None:
        """Delete user"""
        self.user_repository.delete(username)


class DeviceServiceWithGateway:
    """Device service using DTO/Gateway pattern"""

    def __init__(self):
        self.device_repository = DjangoDeviceRepositoryWithGateway()

    def register_device(self, name: str, device_type: str, platform: str, username: str) -> DeviceEntity:
        """Register a new device for a user"""
        # Check if device with same name already exists for this user
        existing_device = self.device_repository.find_by_name_and_user(name, username)
        if existing_device:
            raise ValueError(f"Device with name '{name}' already exists for user '{username}'")
        
        device_entity = DeviceEntity(
            name=name,
            device_type=device_type,
            platform=platform,
            username=username,
            is_active=True
        )
        return self.device_repository.add(device_entity)

    def get_user_devices(self, username: str) -> List[DeviceEntity]:
        """Get all devices for a user"""
        return self.device_repository.find_by_user(username)

    def get_device(self, name: str, username: str) -> Optional[DeviceEntity]:
        """Get specific device by name and user"""
        return self.device_repository.find_by_name_and_user(name, username)

    def update_device(self, device: DeviceEntity) -> DeviceEntity:
        """Update device information"""
        return self.device_repository.update(device)

    def deactivate_device(self, device_id: int) -> None:
        """Deactivate a device"""
        device = self.device_repository.find_by_id(device_id)
        if device:
            device.is_active = False
            self.device_repository.update(device)

    def delete_device(self, device_id: int) -> None:
        """Delete a device"""
        self.device_repository.delete_by_id(device_id)


class SessionServiceWithGateway:
    """Session service using DTO/Gateway pattern"""

    def __init__(self):
        self.session_repository = DjangoSessionRepositoryWithGateway()

    def create_session(self, session_token: str, username: str, 
                      device_name: Optional[str] = None, ip_address: Optional[str] = None,
                      user_agent: Optional[str] = None) -> SessionEntity:
        """Create a new session"""
        session_entity = SessionEntity(
            session_token=session_token,
            username=username,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
            is_active=True
        )
        return self.session_repository.add(session_entity)

    def get_session(self, token: str) -> Optional[SessionEntity]:
        """Get session by token"""
        return self.session_repository.find_by_token(token)

    def get_user_sessions(self, username: str, active_only: bool = False) -> List[SessionEntity]:
        """Get all sessions for a user"""
        if active_only:
            return self.session_repository.find_active_by_user(username)
        return self.session_repository.find_by_user(username)

    def update_session_activity(self, token: str) -> None:
        """Update session last activity"""
        self.session_repository.update_last_activity(token)

    def deactivate_session(self, token: str) -> None:
        """Deactivate a session"""
        self.session_repository.deactivate(token)

    def logout_user(self, username: str) -> None:
        """Logout user (deactivate all sessions)"""
        self.session_repository.deactivate_user_sessions(username)

    def cleanup_inactive_sessions(self) -> None:
        """Remove all inactive sessions"""
        self.session_repository.delete_inactive_sessions()
