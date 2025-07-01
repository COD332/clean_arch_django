"""
Gateways for converting between domain entities, DTOs, and Django models.
This implements the Gateway pattern to isolate domain logic from infrastructure concerns.
"""

from typing import List, Optional
from django.contrib.auth.models import User

from ..domain.entities import UserEntity, DeviceEntity, SessionEntity
from ..domain.dtos import UserDTO, DeviceDTO, SessionDTO
from ..models import Device, Session


class UserGateway:
    """Gateway for User entity/DTO/model conversions"""

    @staticmethod
    def entity_to_dto(entity: UserEntity) -> UserDTO:
        """Convert UserEntity to UserDTO"""
        return UserDTO(
            username=entity.username,
            email=entity.email,
            password=entity.password
        )

    @staticmethod
    def dto_to_entity(dto: UserDTO) -> UserEntity:
        """Convert UserDTO to UserEntity"""
        return UserEntity(
            username=dto.username,
            email=dto.email,
            password=dto.password
        )

    @staticmethod
    def dto_to_model(dto: UserDTO) -> User:
        """Convert UserDTO to Django User model"""
        if dto.id:
            # Update existing user
            user = User.objects.get(id=dto.id)
            user.username = dto.username
            user.email = dto.email
            user.is_active = dto.is_active
            if dto.password:
                user.set_password(dto.password)
            return user
        else:
            # Create new user
            return User(
                username=dto.username,
                email=dto.email,
                is_active=dto.is_active
            )

    @staticmethod
    def model_to_dto(model: User) -> UserDTO:
        """Convert Django User model to UserDTO"""
        return UserDTO(
            id=model.id,
            username=model.username,
            email=model.email,
            is_active=model.is_active,
            date_joined=model.date_joined,
            last_login=model.last_login
        )

    @staticmethod
    def model_to_entity(model: User) -> UserEntity:
        """Convert Django User model to UserEntity"""
        return UserEntity(
            username=model.username,
            email=model.email
        )

    @staticmethod
    def entity_to_model_via_dto(entity: UserEntity) -> User:
        """Convert UserEntity to Django User model via DTO"""
        dto = UserGateway.entity_to_dto(entity)
        return UserGateway.dto_to_model(dto)


class DeviceGateway:
    """Gateway for Device entity/DTO/model conversions"""

    @staticmethod
    def entity_to_dto(entity: DeviceEntity, user_id: Optional[int] = None) -> DeviceDTO:
        """Convert DeviceEntity to DeviceDTO"""
        return DeviceDTO(
            id=entity.device_id,
            name=entity.name,
            device_type=entity.device_type,
            platform=entity.platform,
            user_id=user_id,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def dto_to_entity(dto: DeviceDTO, username: Optional[str] = None) -> DeviceEntity:
        """Convert DeviceDTO to DeviceEntity"""
        return DeviceEntity(
            device_id=dto.id,
            name=dto.name,
            device_type=dto.device_type,
            platform=dto.platform,
            username=username or '',
            is_active=dto.is_active,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def dto_to_model(dto: DeviceDTO) -> Device:
        """Convert DeviceDTO to Django Device model"""
        if dto.id:
            # Update existing device
            device = Device.objects.get(id=dto.id)
            device.name = dto.name
            device.device_type = dto.device_type
            device.platform = dto.platform
            device.is_active = dto.is_active
            if dto.user_id:
                device.user_id = dto.user_id
            return device
        else:
            # Create new device
            return Device(
                name=dto.name,
                device_type=dto.device_type,
                platform=dto.platform,
                user_id=dto.user_id,
                is_active=dto.is_active
            )

    @staticmethod
    def model_to_dto(model: Device) -> DeviceDTO:
        """Convert Django Device model to DeviceDTO"""
        return DeviceDTO(
            id=model.id,
            name=model.name,
            device_type=model.device_type,
            platform=model.platform,
            user_id=model.user_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def model_to_entity(model: Device) -> DeviceEntity:
        """Convert Django Device model to DeviceEntity"""
        return DeviceEntity(
            device_id=model.id,
            name=model.name,
            device_type=model.device_type,
            platform=model.platform,
            username=model.user.username,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def entity_to_model_via_dto(entity: DeviceEntity, user_id: int) -> Device:
        """Convert DeviceEntity to Django Device model via DTO"""
        dto = DeviceGateway.entity_to_dto(entity, user_id)
        return DeviceGateway.dto_to_model(dto)


class SessionGateway:
    """Gateway for Session entity/DTO/model conversions"""

    @staticmethod
    def entity_to_dto(entity: SessionEntity, user_id: Optional[int] = None, 
                     device_id: Optional[int] = None) -> SessionDTO:
        """Convert SessionEntity to SessionDTO"""
        return SessionDTO(
            id=entity.session_id,
            session_token=entity.session_token,
            user_id=user_id,
            device_id=device_id,
            ip_address=entity.ip_address,
            user_agent=entity.user_agent,
            is_active=entity.is_active,
            created_at=entity.created_at,
            last_activity=entity.last_activity
        )

    @staticmethod
    def dto_to_entity(dto: SessionDTO, username: Optional[str] = None, 
                     device_name: Optional[str] = None) -> SessionEntity:
        """Convert SessionDTO to SessionEntity"""
        return SessionEntity(
            session_id=dto.id,
            session_token=dto.session_token,
            username=username or '',
            device_name=device_name,
            ip_address=dto.ip_address,
            user_agent=dto.user_agent,
            is_active=dto.is_active,
            created_at=dto.created_at,
            last_activity=dto.last_activity
        )

    @staticmethod
    def dto_to_model(dto: SessionDTO) -> Session:
        """Convert SessionDTO to Django Session model"""
        if dto.id:
            # Update existing session
            session = Session.objects.get(id=dto.id)
            session.session_token = dto.session_token
            session.ip_address = dto.ip_address
            session.user_agent = dto.user_agent
            session.is_active = dto.is_active
            if dto.user_id:
                session.user_id = dto.user_id
            if dto.device_id:
                session.device_id = dto.device_id
            return session
        else:
            # Create new session
            return Session(
                session_token=dto.session_token,
                user_id=dto.user_id,
                device_id=dto.device_id,
                ip_address=dto.ip_address,
                user_agent=dto.user_agent,
                is_active=dto.is_active
            )

    @staticmethod
    def model_to_dto(model: Session) -> SessionDTO:
        """Convert Django Session model to SessionDTO"""
        return SessionDTO(
            id=model.id,
            session_token=model.session_token,
            user_id=model.user_id,
            device_id=model.device_id,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            is_active=model.is_active,
            created_at=model.created_at,
            last_activity=model.last_activity
        )

    @staticmethod
    def model_to_entity(model: Session) -> SessionEntity:
        """Convert Django Session model to SessionEntity"""
        return SessionEntity(
            session_id=model.id,
            session_token=model.session_token,
            username=model.user.username,
            device_name=model.device.name if model.device else None,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            is_active=model.is_active,
            created_at=model.created_at,
            last_activity=model.last_activity
        )

    @staticmethod
    def entity_to_model_via_dto(entity: SessionEntity, user_id: int, 
                               device_id: Optional[int] = None) -> Session:
        """Convert SessionEntity to Django Session model via DTO"""
        dto = SessionGateway.entity_to_dto(entity, user_id, device_id)
        return SessionGateway.dto_to_model(dto)
