from abc import ABC, abstractmethod
from .entities import UserEntity, DeviceEntity
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
