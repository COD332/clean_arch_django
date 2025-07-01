from abc import ABC, abstractmethod
from .entities import UserEntity

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
