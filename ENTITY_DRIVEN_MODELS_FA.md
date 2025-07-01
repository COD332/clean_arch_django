# مدل‌های جنگو مبتنی بر انتیتی

این پروژه الگوی معماری تمیز (Clean Architecture) را پیاده‌سازی می‌کند که در آن مدل‌های جنگو به صورت خودکار از انتیتی‌های دامنه تولید می‌شوند و مشکل رایج نگهداری تعاریف مدل تکراری را حل می‌کند.

## مشکل حل شده

در پیاده‌سازی‌های سنتی معماری تمیز، معمولاً باید ساختار مدل یکسانی را در دو جا نگهداری کنید:
1. انتیتی‌های دامنه (لایه منطق کسب‌وکار)
2. مدل‌های جنگو (لایه زیرساخت)

این موضوع منجر می‌شود به:
- تکرار کد
- بار اضافی نگهداری
- خطر عدم تطابق بین تعاریف انتیتی و مدل

## راه‌حل: تولید مدل مبتنی بر انتیتی

راه‌حل ما به صورت خودکار مدل‌های جنگو را از انتیتی‌های dataclass تولید می‌کند و تضمین می‌کند:
- **منبع واحد حقیقت**: تعاریف انتیتی باعث ایجاد مدل می‌شوند
- **اصل DRY**: بدون تکرار کد
- **ایمنی نوع**: نگاشت خودکار نوع از پایتون به فیلدهای جنگو
- **سازگاری**: مدل‌ها همیشه با انتیتی‌ها مطابقت دارند

## نحوه کارکرد

### 1. تعریف انتیتی شما

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DeviceEntity:
    name: str
    device_type: str
    platform: str
    username: str  # کاربر مرتبط
    is_active: bool = True
    device_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### 2. تولید مدل جنگو

```python
from .domain.entities import DeviceEntity
from .infrastructure.model_generator import create_model_from_entity

# تولید مدل Device از DeviceEntity
Device = create_model_from_entity(
    entity_class=DeviceEntity,
    model_name='Device',
    additional_fields={
        'user': models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices'),
    },
    meta_options={
        'unique_together': ('name', 'user'),
    }
)
```

### 3. استفاده از نگاشت انتیتی-مدل

```python
from .infrastructure.entity_mapper import EntityModelMapper

# تبدیل انتیتی به مدل
entity = DeviceEntity(name="iPhone", device_type="mobile", platform="iOS", username="john")
model_data = EntityModelMapper.entity_to_model_data(entity)
device_model = Device.objects.create(user=user, **model_data)

# تبدیل مدل برگشت به انتیتی
entity = EntityModelMapper.model_to_entity(device_model, DeviceEntity)
```

## اجزای معماری

### 1. رجیستری مدل (`model_registry.py`)
- **ثبت متمرکز**: مکان واحد برای ثبت تمام مدل‌های مبتنی بر انتیتی
- **تضمین سازگاری**: اطمینان از استفاده نمونه‌های یکسان مدل در کل برنامه
- **دسترسی آسان به مدل**: بازیابی مدل‌ها با نام از طریق `ModelRegistry.get_model()`

### 2. تولیدکننده مدل (`infrastructure/model_generator.py`)
- **EntityToModelConverter**: کلاس اصلی برای تبدیل انتیتی‌ها به مدل‌های جنگو
- **نگاشت خودکار نوع**: نگاشت انواع پایتون به فیلدهای مناسب جنگو
- **مدیریت فیلدهای ویژه**: مدیریت timestamps، مقادیر پیش‌فرض و روابط
- **پشتیبانی از گزینه‌های Meta**: پشتیبانی از گزینه‌های Meta مدل جنگو

### 3. نگاشت انتیتی (`infrastructure/entity_mapper.py`)
- **تبدیل دوطرفه**: تبدیل انتیتی ↔ مدل
- **نگاشت فیلد**: مدیریت نگاشت فیلدهای ویژه (مثلاً `device_id` → `id`)
- **عملیات دسته‌ای**: تبدیل لیست مدل‌ها به انتیتی‌ها

### 4. تولیدکننده ادمین (`infrastructure/admin_generator.py`)
- **ایجاد خودکار ادمین**: تولید خودکار پیکربندی ادمین جنگو
- **تشخیص هوشمند فیلد**: دسته‌بندی هوشمند فیلدها برای نمایش
- **قابل سفارشی‌سازی**: امکان تغییر پیکربندی‌های پیش‌فرض

### 5. نگاشت نوع

| نوع پایتون | فیلد جنگو | مدیریت ویژه |
|-------------|--------------|------------------|
| `str` | `CharField` | `max_length` خودکار تشخیص داده می‌شود |
| `int` | `IntegerField` | - |
| `bool` | `BooleanField` | `is_active` پیش‌فرض `True` |
| `datetime` | `DateTimeField` | `created_at` → `auto_now_add=True`<br>`updated_at` → `auto_now=True`<br>`last_activity` → `auto_now=True` |
| `Optional[T]` | `Field(null=True, blank=True)` | - |

### 6. فیلدهای مستثنی

این فیلدهای انتیتی به صورت خودکار از مدل‌های جنگو مستثنی می‌شوند:
- `device_id` → به فیلد خودکار `id` جنگو نگاشت می‌شود
- `username` → از طریق روابط ForeignKey مدیریت می‌شود

## مزایا

### 1. **قابلیت نگهداری**
- تغییر انتیتی → مدل به صورت خودکار به‌روزرسانی می‌شود
- مکان واحد برای تغییر تعاریف فیلد
- کاهش خطر عدم سازگاری

### 2. **تجربه توسعه‌دهنده**
- کمتر کد boilerplate
- ایمنی نوع
- جداسازی واضح نگرانی‌ها

### 3. **مقیاس‌پذیری**
- آسان بودن اضافه کردن انتیتی‌های جدید
- الگوهای سازگار در کل کدبیس
- تولید خودکار فیلد

## مثال: اضافه کردن انتیتی جدید

برای اضافه کردن انتیتی جدید (مثلاً `SessionEntity`):

1. **تعریف انتیتی**:
```python
@dataclass
class SessionEntity:
    session_token: str
    username: str
    ip_address: Optional[str] = None
    is_active: bool = True
    session_id: Optional[int] = None
    created_at: Optional[datetime] = None
```

2. **تولید مدل**:
```python
Session = create_model_from_entity(
    entity_class=SessionEntity,
    model_name='Session',
    additional_fields={
        'user': models.ForeignKey(User, on_delete=models.CASCADE),
    }
)
```

3. **ایجاد migration**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **تولید خودکار رابط ادمین**:
```python
from .infrastructure.admin_generator import register_entity_admin

register_entity_admin(
    model_class=Session,
    entity_class=SessionEntity,
    custom_config={
        'list_display': ('session_token', 'user', 'is_active', 'created_at'),
        'list_filter': ('is_active', 'created_at'),
    }
)
```

همین! نیازی به تعریف دستی مدل جنگو نیست.

## تست

سیستم شامل تست‌های جامع است که پوشش می‌دهد:
- ایجاد و اعتبارسنجی انتیتی
- تولید مدل از انتیتی‌ها
- الگوی Repository با نگاشت خودکار
- endpoint های API
- ادغام رابط ادمین

اجرای تست‌ها با:
```bash
python manage.py test profile_app
```

## ساختار فایل

```
profile_app/
├── domain/
│   ├── entities.py          # انتیتی‌های دامنه (dataclasses)
│   └── repositories.py      # رابط‌های Repository
├── infrastructure/
│   ├── model_generator.py   # تبدیل‌کننده انتیتی → مدل جنگو
│   ├── entity_mapper.py     # ابزارهای نگاشت انتیتی ↔ مدل
│   ├── admin_generator.py   # تولیدکننده ادمین خودکار
│   └── django_*_repository.py # پیاده‌سازی Repository ها
├── use_cases/              # سرویس‌های منطق کسب‌وکار
├── interfaces/             # view ها و serializer های API
├── model_registry.py       # رجیستری متمرکز مدل‌ها
└── models.py              # مدل‌های تولید شده جنگو
```

## مزایای معماری تمیز

این رویکرد اصول معماری تمیز را حفظ می‌کند:

1. **لایه دامنه**: انتیتی‌های کسب‌وکار خالص (بدون وابستگی جنگو)
2. **لایه زیرساخت**: پیاده‌سازی‌های خاص جنگو (مدل‌ها، repository ها)
3. **لایه Use Cases**: منطق کسب‌وکار با استفاده از انتیتی‌های دامنه
4. **لایه رابط**: endpoint های API و serializer ها

رویکرد مبتنی بر انتیتی تضمین می‌کند که دامنه مستقل باقی بماند در حالی که ادغام یکپارچه با ORM جنگو فراهم می‌کند.

## مثال کامل: اضافه کردن سیستم کامنت

بیایید سیستم کامنت کاملی اضافه کنیم:

### گام 1: تعریف انتیتی کامنت

```python
# domain/entities.py
@dataclass
class CommentEntity:
    content: str
    username: str
    device_name: str
    rating: int
    is_approved: bool = False
    comment_id: Optional[int] = None
    created_at: Optional[datetime] = None
```

### گام 2: تعریف رابط Repository

```python
# domain/repositories.py
class CommentRepository(ABC):
    @abstractmethod
    def add(self, comment: CommentEntity) -> CommentEntity:
        ...
    
    @abstractmethod
    def find_by_device(self, device_name: str) -> List[CommentEntity]:
        ...
    
    @abstractmethod
    def approve_comment(self, comment_id: int) -> CommentEntity:
        ...
```

### گام 3: ثبت مدل

```python
# model_registry.py
Comment = ModelRegistry.register_model(
    entity_class=CommentEntity,
    model_name='Comment',
    additional_fields={
        'user': models.ForeignKey(User, on_delete=models.CASCADE),
        'device': models.ForeignKey(Device, on_delete=models.CASCADE),
        'rating': models.IntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(5)]
        ),
    },
    meta_options={
        'ordering': ['-created_at'],
        'unique_together': ('user', 'device'),
    }
)
```

### گام 4: پیاده‌سازی Repository

```python
# infrastructure/django_comment_repository.py
class DjangoCommentRepository(CommentRepository):
    def add(self, comment: CommentEntity) -> CommentEntity:
        user = User.objects.get(username=comment.username)
        device = Device.objects.get(name=comment.device_name, user=user)
        
        model_data = EntityModelMapper.entity_to_model_data(comment)
        model_data.update({'user': user, 'device': device})
        
        django_comment = Comment.objects.create(**model_data)
        return EntityModelMapper.model_to_entity(django_comment, CommentEntity)
    
    def find_by_device(self, device_name: str) -> List[CommentEntity]:
        comments = Comment.objects.filter(device__name=device_name)
        return EntityModelMapper.models_to_entities(comments, CommentEntity)
    
    def approve_comment(self, comment_id: int) -> CommentEntity:
        comment = Comment.objects.get(id=comment_id)
        comment.is_approved = True
        comment.save()
        return EntityModelMapper.model_to_entity(comment, CommentEntity)
```

### گام 5: اضافه کردن ادمین

```python
# admin.py
register_entity_admin(
    model_class=Comment,
    entity_class=CommentEntity,
    custom_config={
        'list_display': ('content', 'rating', 'user', 'device', 'is_approved', 'created_at'),
        'list_filter': ('rating', 'is_approved', 'created_at'),
        'search_fields': ('content', 'user__username', 'device__name'),
        'actions': ['approve_comments'],
    }
)
```

### گام 6: ایجاد Service

```python
# use_cases/comment_service.py
class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo
    
    def add_comment(self, content: str, rating: int, username: str, device_name: str):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        comment = CommentEntity(
            content=content,
            rating=rating,
            username=username,
            device_name=device_name
        )
        return self.repo.add(comment)
    
    def get_device_comments(self, device_name: str):
        return self.repo.find_by_device(device_name)
```

این مثال نشان می‌دهد که چگونه می‌توان به سرعت ویژگی‌های جدید اضافه کرد بدون اینکه نگران تکرار کد یا عدم سازگاری باشید. تمام لایه‌ها از معماری تمیز و الگوی entity-driven استفاده می‌کنند.
