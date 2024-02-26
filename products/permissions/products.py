from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from products.views.products import ProductView
    from products.models.products import Product


class IsProductProviderOrStaff(IsAuthenticated):
    """
    Класс разрешения. Проверяет права пользователя с нужными
    ролями Поставщика либо Персонала.

    И проверяет Поставщика, является ли он поставщиком текущего товара. Если да, то
    он сможет изменить текущий товар. Если нет, то в доступе откажет.
    """
    message = (
        'Вам не разрешено изменять текущее состояние товара! Это разрешение '
        'доступно только Поставщику, который создал данный товар '
        'либо Персоналу магазина!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: ProductView,
            obj: Product
    ) -> bool:
        """
        Проверка поставщика на доступ к конкретному товару.
        Если это персонал, то доступ на изменение товара разрешит.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.provider.user:
            return True
        return False
