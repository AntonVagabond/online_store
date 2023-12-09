from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ExtendedGenericViewSet(GenericViewSet):
    """Расширенный набор общих представлений"""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`
    """
    pass


class CRUListViewSet(ExtendedGenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin):
    """Класс включающий в себя базовые операции, кроме DestroyModelMixin"""
    pass


class CRUDListViewSet(CRUListViewSet,
                      mixins.DestroyModelMixin):
    """Класс включающий в себя CRUD-операции"""
    pass
