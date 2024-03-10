from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .services.utils import is_route_selected
from .views import users
from .views import auth

router = DefaultRouter()

router.register(prefix='', viewset=users.CustomUserViewSet, basename='users')
router.register(prefix=r'search', viewset=users.UserListSearchView, basename='users-search')

urlpatterns = [
    path('auth/jwt/create/', auth.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', auth.CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', auth.CustomTokenVerifyView.as_view(), name='jwt-verify'),
]

# Проверка на разрешенные конечные точки.
selected_user_routes = list(filter(is_route_selected, router.urls))

urlpatterns += (path('users/', include(selected_user_routes)),)
