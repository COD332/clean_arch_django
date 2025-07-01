"""
Data Transfer Objects (DTOs) for the profile domain.
DTOs are used to transfer data between layers and serve as intermediary objects
between domain entities and infrastructure models.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """DTO for User data transfer"""
    id: Optional[int] = None
    username: str = ''
    email: str = ''
    password: str = ''
    is_active: bool = True
    date_joined: Optional[datetime] = None
    last_login: Optional[datetime] = None


@dataclass
class DeviceDTO:
    """DTO for Device data transfer"""
    id: Optional[int] = None
    name: str = ''
    device_type: str = ''
    platform: str = ''
    user_id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class SessionDTO:
    """DTO for Session data transfer"""
    id: Optional[int] = None
    session_token: str = ''
    user_id: Optional[int] = None
    device_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
