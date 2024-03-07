from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from ..models.orders import Order
    from ..views.orders import OrderDetailViewSet


class CurrentUserOrStaff(IsAuthenticated):
    """
    Класс разрешения. Проверяет персонал магазина либо текущего пользователя.
    Если это заказ, текущего пользователя, то он сможет изменить текущий товар.
    Иначе в доступе откажет.
    """
    message = (
        'Вам не разрешено изменять текущее состояние заказа! Это разрешение '
        'доступно только Пользователю, которому принадлежит этот заказ, '
        'либо Персоналу магазина!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: OrderDetailViewSet,
            obj: Order,
    ) -> bool:
        """
        Проверка пользователя на доступ к конкретному заказу.
        Если это персонал, то доступ на изменение товара разрешит.
        """
        if request.user.is_anonymous:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.user:
            return True
        return False
