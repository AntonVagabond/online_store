from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ExtendedGenericViewSet(GenericViewSet):
    """Расширенный набор общих представлений"""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`.
    """
    pass
