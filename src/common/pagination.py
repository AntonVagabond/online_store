from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    """
    Базовая пагинация.

    Аттрибуты:
        * `page_size_query_param` (str)
        * `max_page_size` (int)
    """

    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data) -> Response:
        """Получить ответ с разбивкой по страницам."""

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'results': data
        })
