from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserEntity:
    username: str
    email: str
    password: str = ''

@dataclass
class DeviceEntity:
    name: str
    device_type: str
    platform: str
    username: str  # Associated user
    is_active: bool = True
    device_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class SessionEntity:
    session_token: str
    username: str  # Associated user
    device_name: Optional[str] = None  # Associated device name
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True
    session_id: Optional[int] = None
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
