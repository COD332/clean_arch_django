# DTO/Gateway Pattern Architecture

## Overview

This project has been refactored from an entity-driven model generation approach to a DTO (Data Transfer Object) and Gateway pattern architecture. This change provides better separation of concerns and more explicit control over data transformations between layers.

## Architecture Components

### 1. Domain Layer

#### Entities (`domain/entities.py`)
- **UserEntity**: Core business domain object for users
- **DeviceEntity**: Core business domain object for devices  
- **SessionEntity**: Core business domain object for sessions

Domain entities represent pure business logic and are independent of infrastructure concerns.

#### DTOs (`domain/dtos.py`)
- **UserDTO**: Data transfer object for user data
- **DeviceDTO**: Data transfer object for device data
- **SessionDTO**: Data transfer object for session data

DTOs serve as intermediary objects for data transfer between layers and include infrastructure-specific fields (like IDs and foreign keys).

#### Repository Interfaces (`domain/repositories.py`)
- **UserRepository**: Abstract interface for user persistence
- **DeviceRepository**: Abstract interface for device persistence
- **SessionRepository**: Abstract interface for session persistence

### 2. Infrastructure Layer

#### Django Models (`models.py`)
Explicit Django models that are designed specifically for database persistence:

```python
class Device(models.Model):
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Gateways (`infrastructure/gateways.py`)
Gateway classes handle conversions between entities, DTOs, and Django models:

- **UserGateway**: Converts between UserEntity ↔ UserDTO ↔ Django User
- **DeviceGateway**: Converts between DeviceEntity ↔ DeviceDTO ↔ Django Device  
- **SessionGateway**: Converts between SessionEntity ↔ SessionDTO ↔ Django Session

##### Gateway Methods:
- `entity_to_dto()`: Convert domain entity to DTO
- `dto_to_entity()`: Convert DTO to domain entity
- `dto_to_model()`: Convert DTO to Django model
- `model_to_dto()`: Convert Django model to DTO
- `model_to_entity()`: Direct conversion from Django model to entity
- `entity_to_model_via_dto()`: Convert entity to model via DTO

#### Repository Implementations (`infrastructure/django_repositories_with_gateway.py`)
Concrete implementations of repository interfaces using the gateway pattern:

```python
class DjangoDeviceRepositoryWithGateway(DeviceRepository):
    def add(self, device: DeviceEntity) -> DeviceEntity:
        user = User.objects.get(username=device.username)
        dto = DeviceGateway.entity_to_dto(device, user.id)
        django_device = DeviceGateway.dto_to_model(dto)
        django_device.save()
        return DeviceGateway.model_to_entity(django_device)
```

### 3. Use Cases/Application Layer

#### Services (`use_cases/services_with_gateway.py`)
Service classes that orchestrate business logic using repositories and gateways:

- **UserServiceWithGateway**: User-related operations
- **DeviceServiceWithGateway**: Device management operations
- **SessionServiceWithGateway**: Session management operations

## Data Flow

### Creating a New Device

1. **Application Layer**: Service receives request parameters
2. **Domain Layer**: Creates DeviceEntity with business logic
3. **Gateway**: Converts DeviceEntity → DeviceDTO → Django Device model
4. **Infrastructure**: Persists Django model to database
5. **Gateway**: Converts saved Django model back to DeviceEntity
6. **Application Layer**: Returns DeviceEntity to caller

```
Request → Service → DeviceEntity → Gateway → DeviceDTO → Django Model → Database
                                         ↑                           ↓
Response ← Service ← DeviceEntity ← Gateway ← DeviceDTO ← Django Model
```

## Benefits of This Architecture

### 1. Separation of Concerns
- **Entities**: Pure business logic, no infrastructure dependencies
- **DTOs**: Data transfer between layers with infrastructure fields
- **Models**: Database-specific persistence logic
- **Gateways**: Isolated conversion logic

### 2. Explicit Data Transformations
- Clear conversion points between layers
- Easy to modify data transformation logic
- Better testability of conversion logic

### 3. Infrastructure Independence
- Domain entities are not coupled to Django models
- Can easily swap out Django for another ORM/database
- Domain logic remains pure

### 4. Flexibility
- Can have different DTOs for different use cases
- Models can be optimized for database operations
- Entities can be optimized for business logic

## Migration from Previous Architecture

### Before (Entity-Driven Models)
```python
# Models were generated automatically from entities
Device = ModelRegistry.register_model(
    entity_class=DeviceEntity,
    model_name='Device',
    additional_fields={...}
)
```

### After (DTO/Gateway Pattern)
```python
# Explicit Django model
class Device(models.Model):
    name = models.CharField(max_length=255)
    # ... explicit field definitions

# Gateway for conversions
class DeviceGateway:
    @staticmethod
    def entity_to_dto(entity: DeviceEntity) -> DeviceDTO:
        # Explicit conversion logic
```

## Usage Examples

### Creating a User with Device
```python
# Service layer usage
user_service = UserServiceWithGateway()
device_service = DeviceServiceWithGateway()

# Create user
user = user_service.create_user("john_doe", "john@example.com", "password123")

# Register device for user
device = device_service.register_device(
    name="John's iPhone",
    device_type="mobile",
    platform="iOS",
    username="john_doe"
)
```

### Session Management
```python
session_service = SessionServiceWithGateway()

# Create session
session = session_service.create_session(
    session_token="abc123xyz",
    username="john_doe",
    device_name="John's iPhone",
    ip_address="192.168.1.100"
)

# Update activity
session_service.update_session_activity("abc123xyz")

# Logout user
session_service.logout_user("john_doe")
```

## Testing Strategy

The new architecture makes testing much easier:

1. **Unit Test Entities**: Test pure business logic without infrastructure
2. **Unit Test Gateways**: Test conversion logic in isolation
3. **Integration Test Repositories**: Test with actual database
4. **Mock Gateways**: Mock gateway conversions in service tests

## File Structure

```
apps/profile/
├── domain/
│   ├── entities.py          # Domain entities
│   ├── dtos.py             # Data transfer objects
│   └── repositories.py     # Repository interfaces
├── models.py               # Django models (explicit definitions)
├── infrastructure/
│   ├── gateways.py         # Conversion gateways
│   └── django_repositories_with_gateway.py  # Repository implementations
└── use_cases/
    └── services_with_gateway.py  # Application services
```

This architecture provides a clean, maintainable, and testable codebase that clearly separates business logic from infrastructure concerns while providing explicit control over data transformations.
