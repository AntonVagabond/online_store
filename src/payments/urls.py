from django.urls import path

from .views import payments

urlpatterns = [
    path('orders/payment_confirmation/', payments.PaymentConfirmationAPIView.as_view(), name='payment_confirmation')
]
