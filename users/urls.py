from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users
from users.views import auth

router = DefaultRouter()

router.register(prefix=r'search', viewset=users.UserListSearchView, basename='users-search')

urlpatterns = [
    path('users/registration/', auth.RegistrationView.as_view(), name='registration'),
    path('users/change-password/', auth.ChangePasswordView.as_view(), name='change_password'),
    path('users/me/', users.MeView.as_view(), name='me'),
    path('users/me/edit/', users.MeUpdateView.as_view(), name='me_edit'),
]

urlpatterns += (path('users/', include(router.urls)),)
