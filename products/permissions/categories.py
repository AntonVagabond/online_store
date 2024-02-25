from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsManagerOrAdmin(BasePermission):
    message = (
        'Вам не доступно данное действие. Это действие доступно '
        'только Менеджеру либо Администратору!'
    )

    def has_permission(self, request: Request, view) -> bool:
        """
        Проверка пользователя на доступ к определённому методу. В том случае, когда
        пользователь запрашивает не безопасный метод, проверяется его роль.
        Если роль ниже положенной, то пользователю в получение метода отказано.

        О безопасных и не безопасных методах можно
        почитать здесь -> https://developer.mozilla.org/ru/docs/Glossary/Safe.
        """
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(
            request.user.is_authenticated and
            request.user.is_staff or
            request.user.is_superuser
        )
