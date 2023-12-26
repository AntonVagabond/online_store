from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserNestedSerializer(serializers.ModelSerializer):
    """Вложенный преобразователь пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number')
