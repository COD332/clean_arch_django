# 🏗️ DTO/Gateway Clean Architecture

<div align="center">
  
  <img src="https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Clean%20Architecture-✅-brightgreen?style=for-the-badge" alt="Clean Architecture"/>
  <img src="https://img.shields.io/badge/Test%20Coverage-100%25-brightgreen?style=for-the-badge" alt="Test Coverage"/>

  <h3>🚀 Advanced Django Development with DTO/Gateway Pattern</h3>
  
</div>

---

## 🌍 Language Selection | انتخاب زبان

<div align="center">

### Choose your preferred language | زبان مورد نظر خود را انتخاب کنید

| Language | زبان | Documentation | مستندات |
|----------|------|---------------|---------|
| 🇺🇸 **English** | English | [📖 Read Documentation](./README-en.md) | English Docs |
| 🇮🇷 **Persian** | فارسی | [📚 خواندن مستندات](./README-fa.md) | مستندات فارسی |

</div>

---

## 🎯 Quick Overview | مرور سریع

<div align="center">

A Django application implementing **Clean Architecture** with an innovative **DTO/Gateway Pattern** that provides explicit separation between domain entities, data transfer objects, and infrastructure models.

یک اپلیکیشن جنگو با پیاده‌سازی **Clean Architecture** و الگوی نوآورانه **DTO/Gateway** که جداسازی صریح بین انتیتی‌های دامنه، اشیاء انتقال داده و مدل‌های زیرساخت ارائه می‌دهد.

</div>

### ✨ Key Features | ویژگی‌های کلیدی

<div align="center">

| Feature | English | Persian | فارسی |
|---------|---------|---------|-------|
| 🏗️ | DTO/Gateway Pattern | الگوی DTO/Gateway | ✅ |
| 🧠 | Explicit Data Transformations | تبدیلات صریح داده | ✅ |
| 🔧 | Clean Separation of Concerns | جداسازی تمیز مسئولیت‌ها | ✅ |
| 📚 | Gateway-based Repositories | Repository های مبتنی بر Gateway | ✅ |
| 🚀 | High Maintainability | قابلیت نگهداری بالا | ✅ |
| 💎 | Testable Architecture | معماری قابل تست | ✅ |

</div>

---

## 🏛️ Architecture Benefits | مزایای معماری

<div align="center">

### Before (Entity-Driven) | قبل (Entity-Driven)
```
❌ Hidden Data Transformations
❌ Automatic Model Generation
❌ Generic Conversion Logic
❌ Implicit Dependencies
⏱️ Less Control over Data Flow
```

### After (DTO/Gateway) | بعد (DTO/Gateway)
```
✅ Explicit Data Transformations
✅ Hand-crafted Models
✅ Gateway-based Conversions
✅ Clear Layer Boundaries
⏱️ Full Control over Data Flow
```

</div>

---

## 🚀 Quick Start | شروع سریع

<div align="center">

### 1️⃣ Define Entity | تعریف Entity
```python
@dataclass
class DeviceEntity:
    name: str
    device_type: str
    platform: str
    username: str
    is_active: bool = True
```

### 2️⃣ Create DTO | ایجاد DTO
```python
@dataclass
class DeviceDTO:
    id: Optional[int] = None
    name: str = ''
    device_type: str = ''
    platform: str = ''
    user_id: Optional[int] = None
    is_active: bool = True
```

### 3️⃣ Implement Gateway | پیاده‌سازی Gateway
```python
class DeviceGateway:
    @staticmethod
    def entity_to_dto(entity: DeviceEntity, user_id: int) -> DeviceDTO:
        return DeviceDTO(name=entity.name, user_id=user_id, ...)
```

### 🎉 Use Services | استفاده از سرویس‌ها
```python
device_service = DeviceServiceWithGateway()
device = device_service.register_device("iPhone", "mobile", "iOS", "john")
```

</div>

---

## 📊 Project Metrics | معیارهای پروژه

<div align="center">

| Metric | Value | معیار | مقدار |
|--------|-------|-------|-------|
| 🏗️ Architecture Pattern | DTO/Gateway | الگوی معماری | DTO/Gateway |
| 🧪 Test Coverage | 100% | پوشش تست | ۱۰۰٪ |
| 🔒 Type Safety | Full | ایمنی تایپ | کامل |
| 🎯 Clean Architecture | Enhanced | Clean Architecture | بهبود یافته |
| 🔧 Maintainability | High | قابلیت نگهداری | بالا |
| 🧩 Testability | Excellent | قابلیت تست | عالی |

</div>

---

## 🔧 Technologies | فناوری‌ها

<div align="center">

| Category | Technologies | دسته‌بندی | فناوری‌ها |
|----------|-------------|----------|-----------|
| Backend | Django 5.0+, Python 3.11+ | بک‌اند | Django 5.0+, Python 3.11+ |
| Architecture | Clean Architecture, DTO/Gateway | معماری | Clean Architecture, DTO/Gateway |
| Testing | Unit Tests, Integration Tests | تست | تست واحد، تست یکپارچگی |
| Database | PostgreSQL, SQLite | پایگاه داده | PostgreSQL, SQLite |
| Development | Poetry, Docker | توسعه | Poetry, Docker |

</div>

---

<div align="center">

## 📚 Full Documentation | مستندات کامل

### 🇺🇸 English Documentation
[![English README](https://img.shields.io/badge/📖_English_README-4285F4?style=for-the-badge&logo=googledocs&logoColor=white)](./README-en.md)

### 🇮🇷 Persian Documentation | مستندات فارسی
[![Persian README](https://img.shields.io/badge/📚_مستندات_فارسی-FF6B35?style=for-the-badge&logo=googledocs&logoColor=white)](./README-fa.md)

---

### 🏗️ Architecture Documentation | مستندات معماری

| English | Persian |
|---------|---------|
| [🏗️ DTO/Gateway Architecture](./DTO_GATEWAY_ARCHITECTURE.md) | [🏗️ معماری DTO/Gateway](./DTO_GATEWAY_ARCHITECTURE_FA.md) |
| [📋 Migration Summary](./MIGRATION_SUMMARY.md) | [📋 خلاصه مهاجرت](./MIGRATION_SUMMARY_FA.md) |
| [📁 Final Project Structure](./FINAL_PROJECT_STRUCTURE.md) | [📁 ساختار نهایی پروژه](./FINAL_PROJECT_STRUCTURE_FA.md) |

---

<p align="center">
  <strong>Made with ❤️ and Django | ساخته شده با ❤️ و جنگو</strong><br>
  <a href="https://github.com/cod332/clean_arch_django">⭐ Give it a star | ستاره دهید</a>
</p>

</div>
