# معماری DTO/Gateway

## مرور کلی

این پروژه از الگوی Entity-Driven برای تولید مدل به الگوی معماری **DTO (Data Transfer Object)** و **Gateway** بازنویسی شده است. این تغییر جداسازی بهتری از مسئولیت‌ها و کنترل صریح‌تری بر تبدیلات داده بین لایه‌ها ارائه می‌دهد.

## اجزای معماری

### 1. لایه دامنه

#### انتیتی‌ها (`domain/entities.py`)
- **UserEntity**: شیء دامنه کسب‌وکار اصلی برای کاربران
- **DeviceEntity**: شیء دامنه کسب‌وکار اصلی برای دستگاه‌ها  
- **SessionEntity**: شیء دامنه کسب‌وکار اصلی برای جلسات

انتیتی‌های دامنه منطق کسب‌وکار خالص را نمایندگی می‌کنند و مستقل از نگرانی‌های زیرساخت هستند.

#### DTOها (`domain/dtos.py`)
- **UserDTO**: شیء انتقال داده برای داده‌های کاربر
- **DeviceDTO**: شیء انتقال داده برای داده‌های دستگاه
- **SessionDTO**: شیء انتقال داده برای داده‌های جلسه

DTOها به عنوان اشیاء واسطه برای انتقال داده بین لایه‌ها خدمت می‌کنند و شامل فیلدهای مخصوص زیرساخت (مثل IDها و کلیدهای خارجی) هستند.

#### رابط‌های Repository (`domain/repositories.py`)
- **UserRepository**: رابط انتزاعی برای ماندگاری کاربر
- **DeviceRepository**: رابط انتزاعی برای ماندگاری دستگاه
- **SessionRepository**: رابط انتزاعی برای ماندگاری جلسه

### 2. لایه زیرساخت

#### مدل‌های جنگو (`models.py`)
مدل‌های جنگو صریح که به طور خاص برای ماندگاری پایگاه داده طراحی شده‌اند:

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

#### Gateway ها (`infrastructure/gateways.py`)
کلاس‌های Gateway تبدیلات بین انتیتی‌ها، DTOها و مدل‌های جنگو را مدیریت می‌کنند:

- **UserGateway**: تبدیل بین UserEntity ↔ UserDTO ↔ Django User
- **DeviceGateway**: تبدیل بین DeviceEntity ↔ DeviceDTO ↔ Django Device  
- **SessionGateway**: تبدیل بین SessionEntity ↔ SessionDTO ↔ Django Session

##### متدهای Gateway:
- `entity_to_dto()`: تبدیل انتیتی دامنه به DTO
- `dto_to_entity()`: تبدیل DTO به انتیتی دامنه
- `dto_to_model()`: تبدیل DTO به مدل جنگو
- `model_to_dto()`: تبدیل مدل جنگو به DTO
- `model_to_entity()`: تبدیل مستقیم از مدل جنگو به انتیتی
- `entity_to_model_via_dto()`: تبدیل انتیتی به مدل از طریق DTO

#### پیاده‌سازی Repository ها (`infrastructure/django_repositories_with_gateway.py`)
پیاده‌سازی‌های عینی رابط‌های repository با استفاده از الگوی gateway:

```python
class DjangoDeviceRepositoryWithGateway(DeviceRepository):
    def add(self, device: DeviceEntity) -> DeviceEntity:
        user = User.objects.get(username=device.username)
        dto = DeviceGateway.entity_to_dto(device, user.id)
        django_device = DeviceGateway.dto_to_model(dto)
        django_device.save()
        return DeviceGateway.model_to_entity(django_device)
```

### 3. لایه کاربردها/Use Cases

#### سرویس‌ها (`use_cases/services_with_gateway.py`)
کلاس‌های سرویس که منطق کسب‌وکار را با استفاده از repository ها و gateway ها تنظیم می‌کنند:

- **UserServiceWithGateway**: عملیات مرتبط با کاربر
- **DeviceServiceWithGateway**: عملیات مدیریت دستگاه
- **SessionServiceWithGateway**: عملیات مدیریت جلسه

## جریان داده

### ایجاد دستگاه جدید

1. **لایه اپلیکیشن**: سرویس پارامترهای درخواست را دریافت می‌کند
2. **لایه دامنه**: DeviceEntity با منطق کسب‌وکار ایجاد می‌کند
3. **Gateway**: DeviceEntity → DeviceDTO → مدل جنگو Device را تبدیل می‌کند
4. **زیرساخت**: مدل جنگو را در پایگاه داده ذخیره می‌کند
5. **Gateway**: مدل جنگو ذخیره شده را برگشت به DeviceEntity تبدیل می‌کند
6. **لایه اپلیکیشن**: DeviceEntity را به فراخواننده برمی‌گرداند

```
درخواست → سرویس → DeviceEntity → Gateway → DeviceDTO → مدل جنگو → پایگاه داده
                                         ↑                           ↓
پاسخ ← سرویس ← DeviceEntity ← Gateway ← DeviceDTO ← مدل جنگو
```

## مزایای این معماری

### 1. جداسازی مسئولیت‌ها
- **انتیتی‌ها**: منطق کسب‌وکار خالص، بدون وابستگی‌های زیرساخت
- **DTOها**: انتقال داده بین لایه‌ها با فیلدهای زیرساخت
- **مدل‌ها**: منطق ماندگاری مخصوص پایگاه داده
- **Gateway ها**: منطق تبدیل جداگانه

### 2. تبدیلات صریح داده
- نقاط تبدیل واضح بین لایه‌ها
- تغییر آسان منطق تبدیل داده
- قابلیت تست بهتر منطق تبدیل

### 3. استقلال از زیرساخت
- انتیتی‌های دامنه به مدل‌های جنگو وصل نیستند
- می‌توان به راحتی جنگو را با ORM/پایگاه داده دیگری جایگزین کرد
- منطق دامنه خالص باقی می‌ماند

### 4. انعطاف‌پذیری
- می‌توان DTOهای مختلف برای کاربردهای مختلف داشت
- مدل‌ها می‌توانند برای عملیات پایگاه داده بهینه شوند
- انتیتی‌ها می‌توانند برای منطق کسب‌وکار بهینه شوند

## مهاجرت از معماری قبلی

### قبل (مدل‌های Entity-Driven)
```python
# مدل‌ها به صورت خودکار از انتیتی‌ها تولید می‌شدند
Device = ModelRegistry.register_model(
    entity_class=DeviceEntity,
    model_name='Device',
    additional_fields={...}
)
```

### بعد (الگوی DTO/Gateway)
```python
# مدل جنگو صریح
class Device(models.Model):
    name = models.CharField(max_length=255)
    # ... تعاریف صریح فیلد

# Gateway برای تبدیلات
class DeviceGateway:
    @staticmethod
    def entity_to_dto(entity: DeviceEntity) -> DeviceDTO:
        # منطق تبدیل صریح
```

## نمونه‌های استفاده

### ایجاد کاربر با دستگاه
```python
# استفاده از لایه سرویس
user_service = UserServiceWithGateway()
device_service = DeviceServiceWithGateway()

# ایجاد کاربر
user = user_service.create_user("john_doe", "john@example.com", "password123")

# ثبت دستگاه برای کاربر
device = device_service.register_device(
    name="iPhone جان",
    device_type="mobile",
    platform="iOS",
    username="john_doe"
)
```

### مدیریت جلسه
```python
session_service = SessionServiceWithGateway()

# ایجاد جلسه
session = session_service.create_session(
    session_token="abc123xyz",
    username="john_doe",
    device_name="iPhone جان",
    ip_address="192.168.1.100"
)

# به‌روزرسانی فعالیت
session_service.update_session_activity("abc123xyz")

# خروج کاربر
session_service.logout_user("john_doe")
```

## استراتژی تست

معماری جدید تست را بسیار آسان‌تر می‌کند:

1. **تست واحد انتیتی‌ها**: تست منطق کسب‌وکار خالص بدون زیرساخت
2. **تست واحد Gateway ها**: تست منطق تبدیل به صورت جداگانه
3. **تست یکپارچگی Repository ها**: تست با پایگاه داده واقعی
4. **Mock Gateway ها**: Mock کردن تبدیلات gateway در تست‌های سرویس

## ساختار فایل

```
apps/profile/
├── domain/
│   ├── entities.py          # انتیتی‌های دامنه
│   ├── dtos.py             # اشیاء انتقال داده
│   └── repositories.py     # رابط‌های repository
├── infrastructure/
│   ├── gateways.py         # Gateway های تبدیل
│   └── django_repositories_with_gateway.py  # پیاده‌سازی repository
├── use_cases/
│   └── services_with_gateway.py  # سرویس‌های اپلیکیشن
├── models.py                # مدل‌های جنگو صریح
└── admin.py                 # پیکربندی ادمین جنگو
```

این معماری یک کدبیس تمیز، قابل نگهداری و قابل تست ارائه می‌دهد که به وضوح منطق کسب‌وکار را از نگرانی‌های زیرساخت جدا می‌کند و در عین حال کنترل صریح بر تبدیلات داده ارائه می‌دهد.
