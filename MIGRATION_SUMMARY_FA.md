# مهاجرت از مدل‌های Entity-Driven به الگوی DTO/Gateway

## خلاصه

پروژه با موفقیت از رویکرد تولید مدل مبتنی بر انتیتی به معماری تمیز **DTO (Data Transfer Object)** و **Gateway** مهاجرت کرده است. این تغییر جداسازی بهتری از مسئولیت‌ها، تبدیلات صریح داده و بهبود قابلیت نگهداری ارائه می‌دهد.

## آنچه تغییر کرده

### قبل: تولید مدل مبتنی بر انتیتی

#### معماری
```
انتیتی دامنه → تولیدکننده مدل → مدل جنگو → پایگاه داده
```

#### پیاده‌سازی
- **انتیتی‌ها**: اشیاء `@dataclass` که منطق کسب‌وکار را تعریف می‌کنند
- **تولیدکننده مدل**: ایجاد خودکار مدل جنگو از انتیتی‌ها
- **نگاشت انتیتی**: تبدیل ساده بین انتیتی‌ها و مدل‌ها
- **Repository**: تبدیل مستقیم انتیتی ↔ مدل

#### مثال کد (قدیمی)
```python
# انتیتی
@dataclass
class DeviceEntity:
    name: str
    device_type: str
    platform: str
    username: str

# مدل تولید شده خودکار
Device = ModelRegistry.register_model(
    entity_class=DeviceEntity,
    model_name='Device',
    additional_fields={'user': models.ForeignKey(User, ...)},
)

# Repository
class DjangoDeviceRepository:
    def add(self, device: DeviceEntity) -> DeviceEntity:
        model_data = EntityModelMapper.entity_to_model_data(device)
        django_device = Device.objects.create(**model_data)
        return EntityModelMapper.model_to_entity(django_device, DeviceEntity)
```

### بعد: الگوی DTO/Gateway

#### معماری
```
انتیتی دامنه ↔ DTO ↔ مدل جنگو ↔ پایگاه داده
       ↑         ↑         ↑
   Gateway   Gateway   Gateway
```

#### پیاده‌سازی
- **انتیتی‌ها**: اشیاء کسب‌وکار خالص (بدون تغییر)
- **DTOها**: اشیاء انتقال داده با فیلدهای زیرساخت
- **مدل‌های جنگو**: تعاریف صریح مدل
- **Gateway ها**: منطق تبدیل بین انتیتی ↔ DTO ↔ مدل
- **Repository ها**: استفاده از gateway ها برای تمام تبدیلات

#### مثال کد (جدید)
```python
# انتیتی (بدون تغییر)
@dataclass
class DeviceEntity:
    name: str
    device_type: str
    platform: str
    username: str

# DTO
@dataclass
class DeviceDTO:
    id: Optional[int] = None
    name: str = ''
    device_type: str = ''
    platform: str = ''
    user_id: Optional[int] = None
    is_active: bool = True

# مدل جنگو صریح
class Device(models.Model):
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

# Gateway
class DeviceGateway:
    @staticmethod
    def entity_to_dto(entity: DeviceEntity, user_id: int) -> DeviceDTO:
        return DeviceDTO(
            name=entity.name,
            device_type=entity.device_type,
            platform=entity.platform,
            user_id=user_id,
            is_active=entity.is_active
        )

# Repository با Gateway
class DjangoDeviceRepositoryWithGateway:
    def add(self, device: DeviceEntity) -> DeviceEntity:
        user = User.objects.get(username=device.username)
        dto = DeviceGateway.entity_to_dto(device, user.id)
        django_device = DeviceGateway.dto_to_model(dto)
        django_device.save()
        return DeviceGateway.model_to_entity(django_device)
```

## مزایای معماری جدید

### 1. **تبدیلات صریح داده**
- **قبل**: منطق تبدیل مخفی در نگاشت‌های عمومی
- **بعد**: متدهای تبدیل واضح و قابل تست در gateway ها

### 2. **جداسازی بهتر مسئولیت‌ها**
- **لایه دامنه**: منطق کسب‌وکار خالص (انتیتی‌ها)
- **لایه DTO**: انتقال داده با نگرانی‌های زیرساخت
- **لایه زیرساخت**: مدل‌ها و gateway های مخصوص پایگاه داده

### 3. **انعطاف‌پذیری**
- **قبل**: نگاشت یک انتیتی → یک مدل
- **بعد**: چندین DTO برای هر انتیتی، مدل‌های بهینه، تبدیلات انعطاف‌پذیر

### 4. **قابلیت تست**
- **قبل**: تست سخت منطق تبدیل
- **بعد**: هر متد gateway می‌تواند به صورت مستقل تست واحد شود

### 5. **قابلیت نگهداری**
- **قبل**: تغییرات انتیتی‌ها به صورت خودکار بر مدل‌ها تأثیر می‌گذاشت
- **بعد**: کنترل صریح بر تمام تبدیلات داده

## فایل‌های ایجاد شده/تغییر یافته

### فایل‌های جدید
```
apps/profile/domain/dtos.py                           # اشیاء انتقال داده
apps/profile/models.py                                # مدل‌های جنگو صریح
apps/profile/infrastructure/gateways.py              # Gateway های تبدیل
apps/profile/infrastructure/django_repositories_with_gateway.py  # Repository های جدید
apps/profile/use_cases/services_with_gateway.py      # سرویس‌های استفاده از gateway
```

### فایل‌های تغییر یافته
```
apps/profile/models.py                    # به‌روزرسانی import ها
apps/profile/admin.py                     # به‌روزرسانی کلاس‌های ادمین
apps/profile/interfaces/views.py          # به‌روزرسانی برای استفاده از سرویس‌های جدید
apps/profile/domain/repositories.py       # اضافه شدن رابط SessionRepository
```

### فایل‌های پشتیبان‌گیری شده
```
تمام فایل‌های پشتیبان پاک شده و حذف شده‌اند:
- model_registry.py.backup (حذف شده)
- infrastructure/model_generator.py.backup (حذف شده)
- infrastructure/entity_mapper.py.backup (حذف شده)
- infrastructure/admin_generator.py.backup (حذف شده)
- infrastructure/django_device_repository.py.backup (حذف شده)
- infrastructure/django_user_repository.py.backup (حذف شده)
- use_cases/device_service.py.backup (حذف شده)
- use_cases/user_service.py.backup (حذف شده)
- migrations/backup/ (حذف شده)
```

## جزئیات مهاجرت

### طرح پایگاه داده
- **مهاجرت**: `0001_initial_dto_gateway_models.py`
- **تغییرات**: طرح تمیز بر اساس مدل‌های صریح
- **وضعیت**: ✅ با موفقیت اعمال شده

### سرویس‌ها
- **UserServiceWithGateway**: عملیات مدیریت کاربر
- **DeviceServiceWithGateway**: عملیات مدیریت دستگاه  
- **SessionServiceWithGateway**: عملیات مدیریت جلسه

### تست
- **اسکریپت تست**: `test_dto_gateway.py`
- **پوشش**: تمام عملیات CRUD، تبدیلات gateway
- **وضعیت**: ✅ تمام تست‌ها موفق

## نمونه‌های استفاده

### ایجاد کاربر و دستگاه
```python
# مقداردهی اولیه سرویس‌ها
user_service = UserServiceWithGateway()
device_service = DeviceServiceWithGateway()

# ایجاد کاربر
user = user_service.create_user("john", "john@example.com", "password")

# ثبت دستگاه
device = device_service.register_device(
    name="iPhone جان",
    device_type="mobile", 
    platform="iOS",
    username="john"
)
```

### مدیریت جلسه
```python
session_service = SessionServiceWithGateway()

# ایجاد جلسه
session = session_service.create_session(
    session_token="abc123",
    username="john",
    device_name="iPhone جان",
    ip_address="192.168.1.100"
)

# دریافت جلسات کاربر
sessions = session_service.get_user_sessions("john", active_only=True)
```

### استفاده مستقیم Gateway
```python
from apps.profile.infrastructure.gateways import DeviceGateway

# تبدیل بین لایه‌ها
entity = DeviceEntity(name="تست", device_type="mobile", platform="iOS", username="john")
dto = DeviceGateway.entity_to_dto(entity, user_id=1)
model = DeviceGateway.dto_to_model(dto)
```

## ملاحظات عملکرد

### قبل
- تولید مدل بر اساس reflection
- منطق تبدیل عمومی
- کوئری‌های پایگاه داده کمتر بهینه

### بعد  
- مدل‌های صریح و بهینه
- متدهای تبدیل هدفمند
- فرصت‌های بهتر بهینه‌سازی کوئری
- انتقال داده کارآمدتر

## گام‌های بعدی

1. **لایه API**: به‌روزرسانی serializer ها برای کار با سرویس‌های جدید
2. **احراز هویت**: پیاده‌سازی احراز هویت مبتنی بر جلسه با استفاده از SessionService
3. **اعتبارسنجی**: اضافه کردن منطق اعتبارسنجی DTO
4. **کش**: پیاده‌سازی کش در سطح DTO
5. **تست**: گسترش پوشش تست برای تمام متدهای gateway

## مستندات

- **راهنمای معماری**: `DTO_GATEWAY_ARCHITECTURE_FA.md`
- **نمونه‌های تست**: `test_dto_gateway.py`
- **تاریخچه مهاجرت**: فایل‌های پشتیبان برای مرجع حفظ شده

مهاجرت کامل شده و الگوی جدید DTO/Gateway معماری بسیار تمیزتر و قابل نگهداری‌تری ارائه می‌دهد در حالی که تمام عملکردهای موجود را حفظ می‌کند.
