from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models.base import CustomToken

User = get_user_model()


class AuthUserSerializer(serializers.ModelSerializer):
    """Внутренний преобразователь для аутентификации."""
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'is_active', 'is_staff')
        read_only_fields = ('id', 'is_active', 'is_staff')

    @staticmethod
    def get_auth_token(obj: type[User]):
        token = CustomToken.objects.get(user=obj)
        return token.key
