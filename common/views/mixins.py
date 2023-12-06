from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListViewSet(GenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`
    """
    pass
