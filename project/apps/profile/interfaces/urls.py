from django.urls import path
from .views import *

urlpatterns = [
    # User endpoints
    path('register/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('delete/', DeleteUserView.as_view()),
    
    # Device endpoints
    path('devices/', CreateDeviceView.as_view()),  # POST to create device
    path('devices/list/', UserDevicesView.as_view()),  # GET to list user's devices
    path('devices/<int:device_id>/', DeviceDetailView.as_view()),  # GET, PUT, DELETE specific device
    path('devices/<int:device_id>/deactivate/', DeactivateDeviceView.as_view()),  # POST to deactivate device
]
