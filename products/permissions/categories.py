from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

if TYPE_CHECKING:
    from products.views.categories import CategoryView


class IsManagerOrAdmin(BasePermission):
    """
    Класс разрешения для проверки прав пользователя с ролями Менеджера или Админа.
    """
    message = (
        'Вам не доступно данное действие. Это действие доступно '
        'только Менеджеру либо Администратору!'
    )

    def has_permission(self, request: Request, view: CategoryView) -> bool:
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
