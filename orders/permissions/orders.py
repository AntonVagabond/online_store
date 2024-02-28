from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from orders.models.orders import Order
    from orders.views.orders import OrderDetailViewSet


class CurrentUserOrStaff(IsAuthenticated):
    """
    ����� ����������. ��������� �������� �������� ���� �������� ������������.
    ���� ��� �����, �������� ������������, �� �� ������ �������� ������� �����.
    ����� � ������� �������.
    """
    message = (
        '��� �� ��������� �������� ������� ��������� ������! ��� ���������� '
        '�������� ������ ������������, �������� ����������� ���� �����, '
        '���� ��������� ��������!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: OrderDetailViewSet,
            obj: Order,
    ) -> bool:
        """
        �������� ������������ �� ������ � ����������� ������.
        ���� ��� ��������, �� ������ �� ��������� ������ ��������.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.user:
            return True
        return False
