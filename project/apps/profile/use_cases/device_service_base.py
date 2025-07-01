from abc import ABC, abstractmethod
from typing import List

class DeviceServiceBase(ABC):
    @abstractmethod
    def create_device(self, name: str, device_type: str, platform: str, username: str):
        ...

    @abstractmethod
    def get_user_devices(self, username: str):
        ...

    @abstractmethod
    def get_device_by_id(self, device_id: int):
        ...

    @abstractmethod
    def update_device(self, device_id: int, name: str = None, device_type: str = None, 
                      platform: str = None, is_active: bool = None):
        ...

    @abstractmethod
    def delete_device(self, device_id: int):
        ...

    @abstractmethod
    def deactivate_device(self, device_id: int):
        ...
