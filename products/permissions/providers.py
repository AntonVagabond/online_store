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
    ����� ����������. ���� ������ ������ ��� ������. ���� ������ �� ���������, ��
    ����� �������� ���� ������������ � ������� ������ ���������� ���� ���������.
    """
    message = (
        '��� �� �������� ������ ��������. ��� �������� �������� '
        '������ ���������� ���� ��������� ��������!'
    )

    def has_permission(
            self,
            request: Request,
            view: Union[ProductView, ProviderView],
    ) -> bool:
        """
        �������� ������������ �� ������ � ������������ ������. � �� ����������
        ������� ��������� ���������� ������ ������������� � ����� ���������� ����
        ���� ���������� ��������.

        � ���������� � �� ���������� ������� �����
        �������� ����� -> https://developer.mozilla.org/ru/docs/Glossary/Safe.
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
    ����� ����������. ��������� ����� ������������ � �������
    ������ ���������� ���� ���������.

    � ���������, �������� �� ������������ ���������� �������� ����������.
    ���� ��, �� �� ������ �������� ������ ����������. ���� ���, �� � ������� �������.
    """
    message = (
        '��� �� ��������� �������� ������� ��������� ����������! ��� ���������� '
        '�������� ������ ��������� �������� ���������� ���� ��������� ��������!'
    )

    def has_object_permission(
            self,
            request: Request,
            view: ProductView,
            obj: Provider
    ) -> bool:
        """
        �������� ������������ �� ������ � ����������� ����������.
        ���� ��� ��������, �� ������ �� ��������� ������ ���������� ��������.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.user == obj.user:
            return True
        return False
