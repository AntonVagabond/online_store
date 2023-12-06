from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users

router = DefaultRouter()

router.register(prefix=r'search', viewset=users.UserListSearchView, basename='users-search')

urlpatterns = [
    path('users/registration/', users.RegistrationView.as_view(), name='registration'),
    path('users/me/', users.MeView.as_view(), name='me'),
    path('users/change-password/', users.ChangePasswordView.as_view(), name='change_password'),
]

urlpatterns += (path('users/', include(router.urls)),)
