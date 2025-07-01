from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    CreateUserSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    CreateDeviceSerializer,
    UpdateDeviceSerializer,
    DeviceSerializer,
)
from ..use_cases.user_service import UserService
from ..use_cases.device_service import DeviceService
from ..infrastructure.django_user_repository import DjangoUserRepository
from ..infrastructure.django_device_repository import DjangoDeviceRepository


repo = DjangoUserRepository()
user_service = UserService(repo)

device_repo = DjangoDeviceRepository()
device_service = DeviceService(device_repo)


class CreateUserView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a new user",
        request_body=CreateUserSerializer,
        responses={
            201: openapi.Response('Created', UserSerializer),
            400: 'Validation Error'
        },
    )
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = user_service.create_user(**serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Login and return token (also set cookie)",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('OK', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'token': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: 'Validation Error',
            401: 'Invalid credentials'
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = user_service.login_user(**serializer.validated_data)
        except ValueError:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        resp = Response({'token': token}, status=status.HTTP_200_OK)
        # set the token in a secure, HTTP-only cookie
        resp.set_cookie(
            key='auth_token',
            value=token,
            httponly=True,
            secure=True,      # set False if you’re not on HTTPS in dev
            samesite='Lax',   # or 'Strict' depending on your needs
            max_age=60*60*24  # e.g. 1 day
        )
        return resp


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Change password for the authenticated user",
        request_body=ChangePasswordSerializer,
        responses={
            200: 'Password changed',
            400: 'Validation Error',
            401: 'Authentication credentials were not provided or are invalid'
        },
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_service.change_password(request.user, serializer.validated_data['new_password'])
            return Response({'detail': 'Password changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete the authenticated user",
        responses={
            204: 'User deleted',
            401: 'Authentication credentials were not provided or are invalid'
        },
    )
    def delete(self, request):
        user_service.delete_user(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Device Views
class CreateDeviceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new device for the authenticated user",
        request_body=CreateDeviceSerializer,
        responses={
            201: openapi.Response('Created', DeviceSerializer),
            400: 'Validation Error',
            401: 'Authentication credentials were not provided or are invalid'
        },
    )
    def post(self, request):
        serializer = CreateDeviceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                device = device_service.create_device(
                    username=request.user.username,
                    **serializer.validated_data
                )
                # Convert entity to dict for serializer
                device_data = {
                    'id': device.device_id,
                    'name': device.name,
                    'device_type': device.device_type,
                    'platform': device.platform,
                    'username': device.username,
                    'is_active': device.is_active,
                    'created_at': device.created_at,
                    'updated_at': device.updated_at
                }
                return Response(device_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDevicesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get all devices for the authenticated user",
        responses={
            200: openapi.Response('OK', DeviceSerializer(many=True)),
            401: 'Authentication credentials were not provided or are invalid'
        },
    )
    def get(self, request):
        devices = device_service.get_user_devices(request.user.username)
        devices_data = [
            {
                'id': device.device_id,
                'name': device.name,
                'device_type': device.device_type,
                'platform': device.platform,
                'username': device.username,
                'is_active': device.is_active,
                'created_at': device.created_at,
                'updated_at': device.updated_at
            }
            for device in devices
        ]
        return Response(devices_data, status=status.HTTP_200_OK)


class DeviceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _get_user_device(self, device_id, username):
        """Helper method to get device and verify ownership"""
        try:
            device = device_service.get_device_by_id(device_id)
            if device.username != username:
                return None
            return device
        except ValueError:
            return None

    @swagger_auto_schema(
        operation_summary="Get a specific device by ID",
        responses={
            200: openapi.Response('OK', DeviceSerializer),
            401: 'Authentication credentials were not provided or are invalid',
            404: 'Device not found or not owned by user'
        },
    )
    def get(self, request, device_id):
        device = self._get_user_device(device_id, request.user.username)
        if not device:
            return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        device_data = {
            'id': device.device_id,
            'name': device.name,
            'device_type': device.device_type,
            'platform': device.platform,
            'username': device.username,
            'is_active': device.is_active,
            'created_at': device.created_at,
            'updated_at': device.updated_at
        }
        return Response(device_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a specific device by ID",
        request_body=UpdateDeviceSerializer,
        responses={
            200: openapi.Response('Updated', DeviceSerializer),
            400: 'Validation Error',
            401: 'Authentication credentials were not provided or are invalid',
            404: 'Device not found or not owned by user'
        },
    )
    def put(self, request, device_id):
        device = self._get_user_device(device_id, request.user.username)
        if not device:
            return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateDeviceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_device = device_service.update_device(device_id, **serializer.validated_data)
                device_data = {
                    'id': updated_device.device_id,
                    'name': updated_device.name,
                    'device_type': updated_device.device_type,
                    'platform': updated_device.platform,
                    'username': updated_device.username,
                    'is_active': updated_device.is_active,
                    'created_at': updated_device.created_at,
                    'updated_at': updated_device.updated_at
                }
                return Response(device_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a specific device by ID",
        responses={
            204: 'Device deleted',
            401: 'Authentication credentials were not provided or are invalid',
            404: 'Device not found or not owned by user'
        },
    )
    def delete(self, request, device_id):
        device = self._get_user_device(device_id, request.user.username)
        if not device:
            return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        
        device_service.delete_device(device_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeactivateDeviceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Deactivate a specific device by ID",
        responses={
            200: openapi.Response('Device deactivated', DeviceSerializer),
            401: 'Authentication credentials were not provided or are invalid',
            404: 'Device not found or not owned by user'
        },
    )
    def post(self, request, device_id):
        try:
            device = device_service.get_device_by_id(device_id)
            if device.username != request.user.username:
                return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
            
            updated_device = device_service.deactivate_device(device_id)
            device_data = {
                'id': updated_device.device_id,
                'name': updated_device.name,
                'device_type': updated_device.device_type,
                'platform': updated_device.platform,
                'username': updated_device.username,
                'is_active': updated_device.is_active,
                'created_at': updated_device.created_at,
                'updated_at': updated_device.updated_at
            }
            return Response(device_data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
