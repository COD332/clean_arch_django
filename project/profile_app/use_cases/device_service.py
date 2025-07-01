from .device_service_base import DeviceServiceBase
from profile_app.domain.repositories import DeviceRepository
from profile_app.domain.entities import DeviceEntity
from typing import List

class DeviceService(DeviceServiceBase):
    def __init__(self, repo: DeviceRepository):
        self.repo = repo

    def create_device(self, name: str, device_type: str, platform: str, username: str):
        # Check if device with same name already exists for this user
        existing_device = self.repo.find_by_name_and_user(name, username)
        if existing_device:
            raise ValueError(f"Device with name '{name}' already exists for user '{username}'")
        
        device = DeviceEntity(
            name=name,
            device_type=device_type,
            platform=platform,
            username=username
        )
        return self.repo.add(device)

    def get_user_devices(self, username: str) -> List[DeviceEntity]:
        return self.repo.find_by_user(username)

    def get_device_by_id(self, device_id: int) -> DeviceEntity:
        device = self.repo.find_by_id(device_id)
        if not device:
            raise ValueError(f"Device with ID {device_id} not found")
        return device

    def update_device(self, device_id: int, name: str = None, device_type: str = None, 
                      platform: str = None, is_active: bool = None) -> DeviceEntity:
        device = self.get_device_by_id(device_id)
        
        # Check if new name conflicts with existing devices for the same user
        if name and name != device.name:
            existing_device = self.repo.find_by_name_and_user(name, device.username)
            if existing_device:
                raise ValueError(f"Device with name '{name}' already exists for user '{device.username}'")
        
        # Update only provided fields
        if name is not None:
            device.name = name
        if device_type is not None:
            device.device_type = device_type
        if platform is not None:
            device.platform = platform
        if is_active is not None:
            device.is_active = is_active
        
        return self.repo.update(device)

    def delete_device(self, device_id: int):
        device = self.get_device_by_id(device_id)  # Verify device exists
        self.repo.delete(device_id)

    def deactivate_device(self, device_id: int):
        return self.update_device(device_id, is_active=False)
