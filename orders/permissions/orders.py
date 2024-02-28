from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from orders.models.orders import Order
    from orders.views.orders import OrderDetailViewSet


class CurrentUserOrStaff(IsAuthenticated):
    """
     ласс разрешени€. ѕровер€ет персонал магазина либо текущего пользовател€.
    ≈сли это заказ, текущего пользовател€, то он сможет изменить текущий товар.
    »наче в доступе откажет.
    """
    message = (
        '¬ам не разрешено измен€ть текущее состо€ние заказа! Ёто разрешение '
        'доступно только ѕользователю, которому принадлежит этот заказ, '
        'либо ѕерсоналу магазина!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: OrderDetailViewSet,
            obj: Order,
    ) -> bool:
        """
        ѕроверка пользовател€ на доступ к конкретному заказу.
        ≈сли это персонал, то доступ на изменение товара разрешит.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.user:
            return True
        return False
