from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional

if TYPE_CHECKING:
    from django.urls import URLPattern
    from rest_framework.request import Request
    from ..models.users import User


def is_route_selected(url_pattern: URLPattern) -> bool:
    """
    Проверка на выбранную конечную точку.
    Если есть точки, которые входят в неразрешенный список (unauthorised_urls),
    то они не будут отображаться на схеме.
    """
    unauthorised_urls = (
        '',
        'resend_activation/',
        'reset_username/',
        'reset_username_confirm/',
        'set_password/',
        'set_username/',
    )
    for url in unauthorised_urls:
        match = url_pattern.resolve(url)
        if match:
            return False
    return True


def get_context(
        user: User, request: Request, send_email: bool
) -> Optional[dict[str, Union[str, int]]]:
    """Получить контекст для отправки электронного письма."""
    if send_email:
        context = {
            'user_id': user.pk,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
            'site_name': request.get_host(),
        }
        return context
