from abc import ABC, abstractmethod
from .entities import UserEntity, DeviceEntity, SessionEntity
from typing import List

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def find_by_username(self, username: str) -> UserEntity | None:
        ...

    @abstractmethod
    def delete(self, username: str) -> None:
        ...

    @abstractmethod
    def change_password(self, username: str, new_password: str) -> None:
        ...

class DeviceRepository(ABC):
    @abstractmethod
    def add(self, device: DeviceEntity) -> DeviceEntity:
        ...

    @abstractmethod
    def find_by_id(self, device_id: int) -> DeviceEntity | None:
        ...

    @abstractmethod
    def find_by_user(self, username: str) -> List[DeviceEntity]:
        ...

    @abstractmethod
    def update(self, device: DeviceEntity) -> DeviceEntity:
        ...

    @abstractmethod
    def delete(self, device_id: int) -> None:
        ...

    @abstractmethod
    def find_by_name_and_user(self, name: str, username: str) -> DeviceEntity | None:
        ...

    @abstractmethod
    def delete_by_id(self, device_id: int) -> None:
        ...

    @abstractmethod
    def set_active_status(self, name: str, username: str, is_active: bool) -> None:
        ...

class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: SessionEntity) -> SessionEntity:
        ...

    @abstractmethod
    def find_by_token(self, token: str) -> SessionEntity | None:
        ...

    @abstractmethod
    def find_by_user(self, username: str) -> List[SessionEntity]:
        ...

    @abstractmethod
    def find_active_by_user(self, username: str) -> List[SessionEntity]:
        ...

    @abstractmethod
    def update_last_activity(self, token: str) -> None:
        ...

    @abstractmethod
    def deactivate(self, token: str) -> None:
        ...

    @abstractmethod
    def deactivate_user_sessions(self, username: str) -> None:
        ...

    @abstractmethod
    def delete(self, token: str) -> None:
        ...

    @abstractmethod
    def delete_inactive_sessions(self) -> None:
        ...
