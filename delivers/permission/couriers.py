from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from delivers.models.delivers import Delivery
    from delivers.views.delivery import DeliveryViewSet


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
            view: DeliveryViewSet,
            obj: Delivery
    ):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.courier.user:
            return True
        return False
