from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional

from django.db import transaction
from django.utils import timezone
from djoser import signals
from djoser.conf import settings

from users.views import users as users_views
from users.services.tasks import tasks

if TYPE_CHECKING:
    from users.models.users import User
    from users.serializers.api.users import CustomPasswordResetConfirmSerializer


class UserSignalActivationService:
    """Сервисная часть для сигнала об активации пользователя."""

    def __init__(self, user: User) -> None:
        """Инициализация класса сигнала об активации пользователя."""
        self._user = user

    def signal_user_activation(self) -> None:
        """Отправить сигнал об активации пользователя."""
        signals.user_activated.send(
            sender=users_views.CustomUserViewSet,
            user=self._user,
            request=users_views.CustomUserViewSet.request,
        )


class UserRegistrationService(UserSignalActivationService):
    """Сервисная часть для регистрации пользователя."""

    def __init__(
            self, user: User, context: Optional[dict[str, Union[str, int]]]
    ) -> None:
        """Инициализация класса регистрации пользователя."""
        super().__init__(user)
        self._user = user
        self._context = context

    def _send_email_user_registration(self) -> None:
        """Отправить по электронной почте создание пользователя."""
        tasks.send_registration_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить регистрацию пользователя."""
        self.signal_user_activation()
        if settings.SEND_ACTIVATION_EMAIL:
            self._send_email_user_registration()


class UserActivationService(UserSignalActivationService):
    """Сервисная часть для активации пользователя."""

    def __init__(
            self, user: User, context: Optional[dict[str, Union[str, int]]]
    ) -> None:
        """Инициализация класса активации пользователя."""
        super().__init__(user)
        self._user = user
        self._context = context

    def _user_is_active(self) -> None:
        """Установить пользователя, как активного."""
        self._user.is_active = True

    def _user_save(self) -> None:
        """Сохранить пользователя."""
        self._user.save()

    def _send_email_user_activation(self):
        """Отправить по электронной почте активацию пользователя."""
        tasks.send_activation_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить активацию пользователя."""
        with transaction.atomic():
            self._user_is_active()
            self._user_save()

        self.signal_user_activation()
        if settings.SEND_CONFIRMATION_EMAIL:
            self._send_email_user_activation()


class UserResetPasswordService:
    """Сервисная часть для запроса о новом пароле."""

    def __init__(
            self, user: User, context: Optional[dict[str, Union[str, int]]]
    ) -> None:
        """Инициализация активации пользователя."""
        self._user = user
        self._context = context

    def _send_email_user_reset_password(self) -> None:
        """Отправить по электронной почте новый пароль."""
        tasks.send_reset_password_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить отправку нового пароля."""
        # Если пользователь найден, то отправляем сообщение на почту.
        if self._user:
            self._send_email_user_reset_password()


class UserResetPasswordConfirmService:
    """Сервисная часть для сброса пароля и установление нового."""

    def __init__(
            self,
            user: User,
            serializer: CustomPasswordResetConfirmSerializer,
            context: Optional[dict[str, Union[str, int]]],
    ) -> None:
        """Инициализация класса сброса пароля и установление нового."""
        self._user = user
        self._serializer = serializer
        self._context = context

    def _set_password(self) -> None:
        """Установить новый пароль."""
        self._user.set_password(self._serializer.data['new_password'])

    def _is_has_last_login(self) -> None:
        """Проверка на атрибут `last_login`, если есть поменять ему время."""
        if hasattr(self._user, 'last_login'):
            self._user.last_login = timezone.now()

    def _user_save(self) -> None:
        """Сохранить пользователя."""
        self._user.save()

    def _send_email_user_reset_password_confirm(self) -> None:
        """Отправить по электронной почте информацию о сбросе пароля."""
        tasks.send_reset_password_confirm_task.delay(
            self._context, [self._user.email]
        )

    def execute(self):
        """Выполнить сброс пароля и установить новый."""
        with transaction.atomic():
            self._set_password()
            self._is_has_last_login()
            self._user_save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            self._send_email_user_reset_password_confirm()
