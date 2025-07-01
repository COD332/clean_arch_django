from abc import ABC, abstractmethod

class UserServiceBase(ABC):
    @abstractmethod
    def create_user(self, username, email, password):
        ...

    @abstractmethod
    def login_user(self, username, password):
        ...

    @abstractmethod
    def change_password(self, user, new_password):
        ...

    @abstractmethod
    def delete_user(self, user):
        ...
