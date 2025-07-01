from django.contrib.auth.models import User
from apps.profile.models import Device
from apps.profile.domain.entities import DeviceEntity
from apps.profile.domain.repositories import DeviceRepository
from .entity_mapper import EntityModelMapper
from typing import List

class DjangoDeviceRepository(DeviceRepository):
    def add(self, device: DeviceEntity) -> DeviceEntity:
        user = User.objects.get(username=device.username)
        
        # Convert entity to model data
        model_data = EntityModelMapper.entity_to_model_data(device)
        model_data['user'] = user
        
        django_device = Device.objects.create(**model_data)
        
        # Convert back to entity
        return EntityModelMapper.model_to_entity(django_device, DeviceEntity)

    def find_by_id(self, device_id: int) -> DeviceEntity | None:
        try:
            device = Device.objects.get(id=device_id)
            return EntityModelMapper.model_to_entity(device, DeviceEntity)
        except Device.DoesNotExist:
            return None

    def find_by_user(self, username: str) -> List[DeviceEntity]:
        devices = Device.objects.filter(user__username=username)
        return EntityModelMapper.models_to_entities(devices, DeviceEntity)

    def update(self, device: DeviceEntity) -> DeviceEntity:
        django_device = Device.objects.get(id=device.device_id)
        
        # Update fields from entity
        model_data = EntityModelMapper.entity_to_model_data(device)
        for field_name, value in model_data.items():
            if hasattr(django_device, field_name):
                setattr(django_device, field_name, value)
        
        django_device.save()
        
        # Convert back to entity
        return EntityModelMapper.model_to_entity(django_device, DeviceEntity)

    def delete(self, device_id: int) -> None:
        Device.objects.filter(id=device_id).delete()

    def find_by_name_and_user(self, name: str, username: str) -> DeviceEntity | None:
        try:
            device = Device.objects.get(name=name, user__username=username)
            return EntityModelMapper.model_to_entity(device, DeviceEntity)
        except Device.DoesNotExist:
            return None
