from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt import views


@extend_schema_view(
    post=extend_schema(
        summary='Создание токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenObtainPairView(views.TokenObtainPairView):
    """Представление для создания токена."""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Обновление токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenRefreshView(views.TokenRefreshView):
    """Представление для обновления токена."""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Проверка токена',
        tags=['Аутентификация'],
    ),
)
class CustomTokenVerifyView(views.TokenVerifyView):
    """Представление проверки токена."""
    pass
