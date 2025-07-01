from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from apps.profile.models import Device, Session
from apps.profile.domain.entities import DeviceEntity, SessionEntity
from apps.profile.infrastructure.django_repositories_with_gateway import (
    DjangoUserRepositoryWithGateway, 
    DjangoDeviceRepositoryWithGateway,
    DjangoSessionRepositoryWithGateway
)
from apps.profile.use_cases.services_with_gateway import (
    UserServiceWithGateway, 
    DeviceServiceWithGateway,
    SessionServiceWithGateway
)

class DeviceEntityTestCase(TestCase):
    def test_device_entity_creation(self):
        device = DeviceEntity(
            name="iPhone 15",
            device_type="mobile",
            platform="iOS",
            username="testuser"
        )
        self.assertEqual(device.name, "iPhone 15")
        self.assertEqual(device.device_type, "mobile")
        self.assertEqual(device.platform, "iOS")
        self.assertEqual(device.username, "testuser")
        self.assertTrue(device.is_active)

class DeviceRepositoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.repo = DjangoDeviceRepositoryWithGateway()

    def test_add_device(self):
        device = DeviceEntity(
            name="Test Device",
            device_type="laptop",
            platform="Windows",
            username="testuser"
        )
        saved_device = self.repo.add(device)
        self.assertIsNotNone(saved_device.device_id)
        self.assertEqual(saved_device.name, "Test Device")

    def test_find_by_user(self):
        # Create a device first
        device = DeviceEntity(
            name="Test Device",
            device_type="laptop",
            platform="Windows",
            username="testuser"
        )
        self.repo.add(device)
        
        devices = self.repo.find_by_user("testuser")
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].name, "Test Device")

class DeviceServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.service = DeviceServiceWithGateway()

    def test_create_device(self):
        device = self.service.register_device(
            name="iPhone 15",
            device_type="mobile",
            platform="iOS",
            username="testuser"
        )
        self.assertEqual(device.name, "iPhone 15")
        self.assertIsNotNone(device.device_id)

    def test_duplicate_device_name_error(self):
        # Create first device
        self.service.register_device(
            name="iPhone 15",
            device_type="mobile",
            platform="iOS",
            username="testuser"
        )
        
        # Try to create device with same name
        with self.assertRaises(ValueError):
            self.service.register_device(
                name="iPhone 15",
                device_type="tablet",
                platform="iOS",
                username="testuser"
            )

class DeviceAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_device_api(self):
        data = {
            "name": "iPhone 15",
            "device_type": "mobile",
            "platform": "iOS"
        }
        response = self.client.post('/api/profile/devices/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "iPhone 15")

    def test_list_user_devices_api(self):
        # Create a device first
        Device.objects.create(
            name="Test Device",
            device_type="laptop",
            platform="Windows",
            user=self.user
        )
        
        response = self.client.get('/api/profile/devices/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_access(self):
        self.client.credentials()  # Remove credentials
        response = self.client.get('/api/profile/devices/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
