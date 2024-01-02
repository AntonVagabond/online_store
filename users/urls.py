from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.utils import is_route_selected
from users.views import users

router = DefaultRouter()

router.register(prefix='', viewset=users.CustomUserViewSet, basename='users')
router.register(prefix=r'search', viewset=users.UserListSearchView, basename='users-search')

urlpatterns = []

# Проверка на разрешенные конечные точки.
selected_user_routes = list(filter(is_route_selected, router.urls))

urlpatterns += (path('users/', include(selected_user_routes)),)
