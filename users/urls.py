from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import users

router = DefaultRouter()

urlpatterns = [
    path('users/registration/', users.RegistrationView.as_view(), name='reg'),
]

urlpatterns += (path('users/', include(router.urls)),)