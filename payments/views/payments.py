from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import permissions, status
from rest_framework.response import Response

from common.views.mixins import ExtendedCreateAPIView
from ..services.webhooks import PaymentConfirmWebHookService
from ..serializers.api import payments as payment_s

if TYPE_CHECKING:
    from rest_framework.request import Request


@extend_schema_view(
    post=extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description='Подтверждение оплаты прошло успешно!'
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description='Плохой запрос'
            )
        },
        summary='Обработать платеж с помощью WebHook',
        tags=['Заказ'],
    ),
)
class PaymentConfirmationAPIView(ExtendedCreateAPIView):
    """Представление подтверждения платежа."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = payment_s.EmptyPaymentSerializer

    def post(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Обработка платежа с помощью webhook-а."""
        with transaction.atomic():
            payment_confirm_webhook = PaymentConfirmWebHookService(request=request)
            payment_confirm_webhook.execute()
        return Response(
            data={'answer': 'Подтверждение оплаты прошло успешно!'},
            status=status.HTTP_200_OK,
        )
