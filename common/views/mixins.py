from typing import Union

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from common.constans import roles


class ExtendedView:
    """Расширенное представление"""
    multi_serializer_class = None
    serializer_class = None
    request = None

    def get_serializer_class(self) -> Union[
        serializer_class, multi_serializer_class, None
    ]:
        """Получить класс преобразователя."""

        # Если не будет этих двух условий, то выскачет ошибка.
        assert self.serializer_class or self.multi_serializer_class, (
                '"%s" should either include `serializer_class`, '
                '`multi_serializer_class`, attribute, or override the '
                '`get_serializer_class()` method.' % self.__class__.__name__
        )
        if not self.multi_serializer_class:
            return self.serializer_class

        # Определить коды ролей пользователя.
        user = self.request.user
        if user.is_anonymous:
            user_roles = (roles.PUBLIC_GROUP,)
        elif user.is_superuser:
            user_roles = (roles.ADMIN_GROUP,)
        else:
            user_roles = set(user.groups.all().values_list('code', flat=True))

        # Определить действие или метод запроса.
        if hasattr(self, 'action') and self.action:
            action = self.action
        else:
            action = self.request.method

        # Пытаюсь получить роль + действие преобразователя.
        for role in user_roles:
            serializer_key = f'{role}__{action}'
            if self.multi_serializer_class.get(serializer_key):
                return self.multi_serializer_class.get(serializer_key)

        # Пытаюсь получить преобразователь ролей.
        for role in user_roles:
            serializer_key = role
            if self.multi_serializer_class.get(serializer_key):
                return self.multi_serializer_class.get(serializer_key)

        # Пытаюсь получить преобразователь действий или значение по умолчанию.
        return self.multi_serializer_class.get(action) or self.serializer_class


class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    """Расширенный набор общих представлений."""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`.
    """
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
