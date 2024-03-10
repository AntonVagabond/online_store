from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from rest_framework.request import Request

User = get_user_model()


# TODO: В чтобы работало, под конец проекта раскомментировать в settings.py MIDDLEWARE

class ActiveUserMiddleware(MiddlewareMixin):
    """Класс для реализации функционала статуса покупателя: В сети/Не в сети."""

    @staticmethod
    def process_request(request: Request) -> None:
        """
        Проверка на авторизацию пользователя, и имеет
        ли его сессия уникальный идентификатор session_key.
        """
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)

            if not last_login:
                User.objects.filter(pk=request.user.id).update(
                    last_login=timezone.now()
                )
                # Устанавливаем кэширование на 300 секунд
                # с текущей датой по ключу last-seen-id-пользователя
                cache.set(cache_key, timezone.now(), 300)
