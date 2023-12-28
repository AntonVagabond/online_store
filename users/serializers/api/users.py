from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from djoser import serializers as djoser_serializers

from users.models.profile import Profile
from users.serializers.nested.profile import (
    ProfileShortSerializer,
    ProfileUpdateSerializer,
)

User = get_user_model()


class MeSerializer(djoser_serializers.UserCreateSerializer):
    """
    Преобразователь пользователя.

    Аттрибуты:
        * `profile` (ProfileShortSerializer): профиль.
    """

    profile = ProfileShortSerializer()

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
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
            'password'
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    """
    Преобразователь обновления пользователя.

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

    def update(
            self,
            instance: User,
            validated_data: dict[str, str],
    ) -> User:
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


class UserListSearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name')
