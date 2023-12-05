from rest_framework import serializers
from users.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь профиля"""

    class Meta:
        model = Profile
        fields = ('photo',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь обновления профиля"""

    class Meta:
        model = Profile
        fields = ('photo',)
