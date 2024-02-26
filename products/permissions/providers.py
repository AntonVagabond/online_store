from __future__ import annotations

from typing import TYPE_CHECKING, Union

from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from products.models.providers import Provider

if TYPE_CHECKING:
    from rest_framework.request import Request
    from products.views.products import ProductView
    from products.views.providers import ProviderView


class IsProviderOrStaffOrReadOnly(BasePermission):
    """
    Класс разрешения. Дает доступ только для чтения. Если запрос на изменение, то
    будет проверка прав пользователя с нужными ролями Поставщика либо Персонала.
    """
    message = (
        'Вам не доступно данное действие. Это действие доступно '
        'только Поставщику либо Персоналу магазина!'
    )

    def has_permission(
            self,
            request: Request,
            view: Union[ProductView, ProviderView],
    ) -> bool:
        """
        Проверка пользователя на доступ к определённому методу. К не безопасным
        методам разрешено обращаться только пользователям с ролью Поставщика либо
        быть персоналом магазина.

        О безопасных и не безопасных методах можно
        почитать здесь -> https://developer.mozilla.org/ru/docs/Glossary/Safe.
        """
        if request.method in SAFE_METHODS:
            return True

        if request.user.role == request.user.Role.PROVIDER:
            return bool(request.user and request.user.is_authenticated)

        return bool(
            request.user.is_authenticated and
            request.user.is_staff or
            request.user.is_superuser
        )


class IsCurrentProviderOrStaff(IsAuthenticated):
    """
    Класс разрешения. Проверяет права пользователя с нужными
    ролями Поставщика либо Персонала.

    И проверяет, является ли Пользователь создателем текущего Поставщика.
    Если да, то он сможет изменить модель поставщика. Если нет, то в доступе откажет.
    """
    message = (
        'Вам не разрешено изменять текущее состояние поставщика! Это разрешение '
        'доступно только создателю текущего Поставщика либо Персоналу магазина!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: ProductView,
            obj: Provider
    ) -> bool:
        """
        Проверка пользователя на доступ к конкретному Поставщику.
        Если это персонал, то доступ на изменение модели Поставщика разрешит.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.user:
            return True
        return False
