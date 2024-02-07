from typing import Optional, Union

from djoser.views import UserViewSet
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet


class ExtendedView:
    """Расширенное представление"""
    permission_classes = (AllowAny,)
    multi_permission_classes = None

    multi_serializer_class = None
    serializer_class = None
    request = None

    def _get_action_or_method(self) -> str:
        """Получить действие или метод запроса."""
        if hasattr(self, 'action') and self.action:
            return self.action
        return self.request.method

    def get_permissions(self) -> Union[permission_classes]:
        """Получить класс разрешения"""

        assert self.permission_classes or self.multi_permission_classes, (
                '"%s" должен либо включать `permission_classes`, '
                '`multi_permission_classes`, атрибут, либо переопределять '
                '`get_permissions()` метод.' % self.__class__.__name__
        )
        if not self.multi_permission_classes:
            return [permission() for permission in self.permission_classes]

        # Определить действие или метод запроса.
        action = self._get_action_or_method()
        permissions = self.multi_permission_classes.get(action)
        if permissions:
            return [permission() for permission in permissions]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self) -> Optional[serializer_class]:
        """Получить класс преобразователя."""

        # Если не будет этих двух условий, то выскачет ошибка.
        assert self.serializer_class or self.multi_serializer_class, (
                '"%s" должен либо включать `serializer_class`, '
                '`multi_serializer_class`, атрибут, либо переопределять '
                '`get_serializer_class()` метод.' % self.__class__.__name__
        )
        if not self.multi_serializer_class:
            return self.serializer_class

        action = self._get_action_or_method()

        # Пытаюсь получить преобразователь действий или значение по умолчанию.
        return self.multi_serializer_class.get(action) or self.serializer_class


class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    """Расширенный набор общих представлений."""
    pass


class ExtendedUserViewSet(ExtendedView, UserViewSet):
    """Расширенное представление пользователя."""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`.
    """
    pass


class CreateViewSet(ExtendedGenericViewSet, mixins.CreateModelMixin):
    """Класс представления включающий в себя Create mixins."""
    pass


class RetrieveListViewSet(ExtendedGenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin):
    """Класс представления включающий в себя List и Retrieve mixins."""
    pass


class CRDListViewSet(ExtendedGenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin):
    """
    Класс представления включающий в себя список, базовые операции,
    кроме UpdateModelMixin.
    """
    pass


class CUDViewSet(ExtendedGenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    """
    Класс представления включающий в себя базовые операции, кроме RetrieveModelMixin.
    """
    pass


class RUDViewSet(ExtendedGenericViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    """
    Класс представления включающий в себя базовые операции, кроме CreateModelMixin.
    """
    pass


class CRUListViewSet(ExtendedGenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin):
    """Класс включающий в себя базовые операции, кроме DestroyModelMixin."""
    pass


class CRUDListViewSet(CRUListViewSet,
                      mixins.DestroyModelMixin):
    """Класс включающий в себя CRUD-операции."""
    pass
