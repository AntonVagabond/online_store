from typing import Optional

from crum import get_current_user
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from djoser import serializers as djoser_serializers

from ...models.profile import Profile
from ..nested.profile import ProfileShortSerializer, ProfileUpdateSerializer

User = get_user_model()


# region -------------------- AUTHORISATION AND REGISTRATION ------------------------
class RegistrationSerializer(djoser_serializers.UserCreateSerializer):
    """
    Сериализатор регистрации пользователей.

    Аттрибуты:
        * `email` (EmailField): почта.
        * `password` (CharField): пароль.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    @staticmethod
    def validate_email(value: str) -> str:
        """Проверка на уникальность почты."""

        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Пользователь с такой почтой уже зарегистрирован!')
        return email


class CustomActivationSerializer(djoser_serializers.ActivationSerializer):
    """Сериализатор для активации пользователя"""
    pass


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор смены пароля.

    Аттрибуты:
        * `old_password` (CharField): старый пароль.
        * `new_password` (CharField): новый пароль.
    """

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Проверка на корректность пароля."""
        user = get_current_user()
        old_password = attrs.pop('old_password')
        if not user.check_password(raw_password=old_password):
            raise ParseError('Проверьте правильность текущего пароля!')
        return attrs

    @staticmethod
    def validate_new_password(password: str) -> str:
        """Проверка на корректность нового пароля."""
        validate_password(password=password)
        return password

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """Обновление пароля в модели User."""
        password = validated_data.pop('new_password')
        # Хэшируем пароль
        instance.set_password(raw_password=password)
        instance.save()
        return instance


class PasswordResetSerializer(djoser_serializers.SendEmailResetSerializer):
    """Сериализатор для запроса о новом пароле на почту."""
    pass


class CustomPasswordResetConfirmSerializer(
    djoser_serializers.PasswordResetConfirmSerializer
):
    """Сериализатор для сброса пароля"""
    pass


# endregion -------------------------------------------------------------------------


# region --------------------------------- USER -------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.

    Аттрибуты:
        * `profile` (ProfileShortSerializer): профиль.
    """

    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
            'date_joined',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления пользователя.

    Аттрибуты:
        * `profile` (ProfileShortSerializer): профиль.
    """

    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
        )

    @staticmethod
    def _update_profile(profile: Profile, data: Optional[str]) -> None:
        """Обновление профиля."""

        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """Обновление в модели пользователя."""
        # Проверка на наличия профиля
        profile_data = validated_data.pop(
            'profile') if 'profile' in validated_data else None

        # Если произойдет какая-то ошибка изменения не применятся
        with transaction.atomic():
            instance = super().update(
                instance=instance, validated_data=validated_data
            )
            # Обновление профиля
            if profile_data:
                self._update_profile(instance.profile, profile_data)

        return instance


class UserUpdateRoleSerializer(serializers.ModelSerializer):
    """Сериализатор обновления роли."""

    class Meta:
        model = User
        fields = ('id', 'role')

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """Обновление роли пользователя."""
        current_role = validated_data.pop('role')
        # Проверка на существующую роль.
        if not any((current_role == role for role, _ in instance.Role.choices)):
            ParseError('Такой роли не существует!')
        instance.role = current_role
        instance.is_staff = True
        instance.save()
        return instance


class UserListSearchSerializer(serializers.ModelSerializer):
    """Сериализатор поиска пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name')

# endregion -------------------------------------------------------------------------
