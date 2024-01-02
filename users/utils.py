from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.urls import URLPattern


def is_route_selected(url_pattern: URLPattern) -> bool:
    """
    Проверка на выбранную конечную точку.
    Если есть точки, которые входят в неразрешенный список (unauthorized_urls),
    то они не будут отображаться на схеме.
    """
    unauthorized_urls = (
        '',
        'resend_activation/',
        'reset_username/',
        'reset_username_confirm/',
        'set_password/',
        'set_username/',
    )
    for url in unauthorized_urls:
        match = url_pattern.resolve(url)
        if match:
            return False
    return True
