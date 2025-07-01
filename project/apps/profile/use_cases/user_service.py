from .user_service_base import UserServiceBase
from apps.profile.domain.repositories import UserRepository
from apps.profile.domain.entities import UserEntity
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class UserService(UserServiceBase):
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, username, email, password):
        return self.repo.add(UserEntity(username, email, password))

    def login_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def change_password(self, user, new_password):
        self.repo.change_password(user.username, new_password)

    def delete_user(self, user):
        self.repo.delete(user.username)
