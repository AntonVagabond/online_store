from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission, SAFE_METHODS

if TYPE_CHECKING:
    from rest_framework.request import Request
    from ..views.categories import CategoryView


class IsStaffOrReadOnly(BasePermission):
    """
    Класс разрешения. Дает доступ только для чтения. Если запрос на изменение, то
    будет проверка прав пользователя с нужными ролями Менеджера либо Админа.
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
            return True
        if request.user.is_anonymous:
            return False
        return bool(
            request.user.is_authenticated and
            request.user.is_staff or
            request.user.is_superuser
        )
