from rest_framework import serializers
from users.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    """Преобразователь профиля"""

    class Meta:
        model = Profile
        fields = ('photo',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Преобразователь обновления профиля"""

    class Meta:
        model = Profile
        fields = ('photo',)
