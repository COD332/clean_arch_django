from django.contrib.auth.models import User
from apps.profile.domain.entities import UserEntity
from apps.profile.domain.repositories import UserRepository

class DjangoUserRepository(UserRepository):
    def add(self, user: UserEntity) -> UserEntity:
        django_user = User.objects.create_user(
            username=user.username,
            email=user.email,
            password=user.password
        )
        return UserEntity(
            username=django_user.username,
            email=django_user.email,
            password=''
        )

    def find_by_username(self, username: str) -> UserEntity | None:
        try:
            u = User.objects.get(username=username)
            return UserEntity(username=u.username, email=u.email)
        except User.DoesNotExist:
            return None

    def delete(self, username: str) -> None:
        User.objects.filter(username=username).delete()

    def change_password(self, username: str, new_password: str) -> None:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
