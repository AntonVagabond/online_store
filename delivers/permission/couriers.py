from __future__ import annotations

from typing import TYPE_CHECKING, Union

from rest_framework.permissions import IsAuthenticated

from delivers.models.couriers import Courier
from delivers.models.delivers import Delivery

if TYPE_CHECKING:
    from rest_framework.request import Request
    from delivers.views.delivers import DeliveryViewSet
    from delivers.views.couriers import CourierViewSet


class IsCourierOrStaff(IsAuthenticated):
    """Класс разрешения. Дает доступ только Курьеру либо Персоналу магазина."""
    message = (
        'Вам не доступно данное действие. Это действие доступно '
        'только Курьеру либо Персоналу магазина!'
    )

    def has_permission(self, request: Request, view: DeliveryViewSet):
        """Проверка пользователя, на права Курьера либо Персонала."""
        if request.user.role == request.user.Role.COURIER:
            return True
        return bool(request.user.is_staff or request.user.is_superuser)


class IsCurrentCourierOrStaff(IsAuthenticated):
    """
    Класс разрешения. Дает доступ на изменение состояния доставки, только
    тому Курьеру, который создал эту доставку либо Персоналу магазина.
    """
    message = (
        'Вам не доступно данное действие. Это действие доступно '
        'только Курьеру, который создал эту доставку либо Персоналу магазина!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: Union[DeliveryViewSet, CourierViewSet],
            obj: Union[Delivery, Courier],
    ):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if isinstance(obj, Delivery) and request.user == obj.courier.user:
            return True
        if isinstance(obj, Courier) and request.user == obj.user:
            return True
        return False
