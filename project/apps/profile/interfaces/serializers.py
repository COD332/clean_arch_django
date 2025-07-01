from rest_framework import serializers
from django.contrib.auth.models import User
from apps.profile.models import Device

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Device Serializers
class CreateDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    device_type = serializers.CharField(max_length=100)
    platform = serializers.CharField(max_length=100)

class UpdateDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    device_type = serializers.CharField(max_length=100, required=False)
    platform = serializers.CharField(max_length=100, required=False)
    is_active = serializers.BooleanField(required=False)

class DeviceSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'platform', 'username', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']
