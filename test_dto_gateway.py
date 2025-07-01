"""
Test script to demonstrate the new DTO/Gateway pattern
Run this with: python manage.py shell < test_dto_gateway.py
"""

from apps.profile.use_cases.services_with_gateway import (
    UserServiceWithGateway,
    DeviceServiceWithGateway,
    SessionServiceWithGateway
)

print("=== Testing DTO/Gateway Pattern ===")

# Initialize services
user_service = UserServiceWithGateway()
device_service = DeviceServiceWithGateway()
session_service = SessionServiceWithGateway()

print("\n1. Creating a user...")
try:
    user = user_service.create_user(
        username="test_user_gateway",
        email="test@example.com",
        password="secure_password"
    )
    print(f"✓ Created user: {user.username} ({user.email})")
except Exception as e:
    print(f"✗ User creation failed: {e}")

print("\n2. Registering devices...")
try:
    device1 = device_service.register_device(
        name="iPhone 15",
        device_type="mobile",
        platform="iOS",
        username="test_user_gateway"
    )
    print(f"✓ Registered device: {device1.name} - {device1.platform}")
    
    device2 = device_service.register_device(
        name="MacBook Pro",
        device_type="laptop",
        platform="macOS",
        username="test_user_gateway"
    )
    print(f"✓ Registered device: {device2.name} - {device2.platform}")
except Exception as e:
    print(f"✗ Device registration failed: {e}")

print("\n3. Getting user devices...")
try:
    devices = device_service.get_user_devices("test_user_gateway")
    print(f"✓ Found {len(devices)} devices for user:")
    for device in devices:
        print(f"  - {device.name} ({device.device_type}, {device.platform})")
except Exception as e:
    print(f"✗ Getting devices failed: {e}")

print("\n4. Creating sessions...")
try:
    session1 = session_service.create_session(
        session_token="abc123xyz456",
        username="test_user_gateway",
        device_name="iPhone 15",
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)"
    )
    print(f"✓ Created session: {session1.session_token[:10]}... for {session1.device_name}")
    
    session2 = session_service.create_session(
        session_token="def789uvw012",
        username="test_user_gateway",
        device_name="MacBook Pro",
        ip_address="192.168.1.101",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    )
    print(f"✓ Created session: {session2.session_token[:10]}... for {session2.device_name}")
except Exception as e:
    print(f"✗ Session creation failed: {e}")

print("\n5. Getting user sessions...")
try:
    sessions = session_service.get_user_sessions("test_user_gateway")
    print(f"✓ Found {len(sessions)} sessions for user:")
    for session in sessions:
        print(f"  - {session.session_token[:10]}... from {session.device_name}")
except Exception as e:
    print(f"✗ Getting sessions failed: {e}")

print("\n6. Testing Gateway conversions...")
try:
    from apps.profile.infrastructure.gateways import DeviceGateway, SessionGateway
    from apps.profile.infrastructure.django_models import Device, Session
    
    # Test direct gateway usage
    django_device = Device.objects.filter(name="iPhone 15").first()
    if django_device:
        # Convert Django model to DTO
        dto = DeviceGateway.model_to_dto(django_device)
        print(f"✓ Converted model to DTO: {dto.name} (ID: {dto.id})")
        
        # Convert DTO to Entity
        entity = DeviceGateway.dto_to_entity(dto, username="test_user_gateway")
        print(f"✓ Converted DTO to Entity: {entity.name} (Device ID: {entity.device_id})")
except Exception as e:
    print(f"✗ Gateway conversion test failed: {e}")

print("\n=== DTO/Gateway Pattern Test Complete ===")
print("\nArchitecture Benefits Demonstrated:")
print("✓ Clean separation between Domain Entities and Infrastructure Models")
print("✓ DTOs serve as intermediary data transfer objects")
print("✓ Gateways handle all conversions between layers")
print("✓ Services use domain entities for business logic")
print("✓ Infrastructure details are hidden from domain layer")
