from rest_framework import serializers

from delivers.models.couriers import Courier
from delivers.models.delivers import Delivery
from orders.models.orders import Order


class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    """
        Преобразователь обновления статуса доставки.
    """

    class Meta:
        model = Delivery
        fields = ('id', 'delivery_status',)

    def update(self, instance: Delivery, validated_data: dict[str, str]) -> Delivery:
        """Обновление статуса заказа."""
        instance.delivery_status = validated_data['delivery_status']
        instance.save()
        return instance


class DeliveryListSerializer(serializers.ModelSerializer):
    """
    Преобразователь списка доставок.

    Атрибуты:
        * 'delivery_status' (SerializerMethodField): метод получения статуса.
    """

    delivery_status = serializers.SerializerMethodField(method_name='get_status')

    class Meta:
        model = Delivery
        fields = (
            'id',
            'order',
            'delivery_method',
            'delivery_status',
            'created_at',
            'updated_at',
            'courier',
            'notes'
        )

    @staticmethod
    def get_status(instance: Delivery) -> str:
        """Получить статус."""
        readable_status = instance.get_readable_status(instance.delivery_status)
        return readable_status


class DeliveryCreateSerializer(serializers.ModelSerializer):
    """
        Преобразователь создания доставки.

        Атрибуты:
            * `order` (PrimaryKeyRelatedField): поле заказа.
            * `courier` (PrimaryKeyRelatedField): поле курьеров.
            * 'notes' (CharField): пометки доставки.
            * 'delivery_method' (CharField): способ доставки.
            * 'delivery_status' (CharField): статус доставки.
            * 'created_at' (DateTimeField): время утверждения доставки.
            * 'updated_at' (DateTimeField): время обновления информации о доставке.

    """
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    courier = serializers.PrimaryKeyRelatedField(queryset=Courier.objects.all())
    notes = serializers.CharField(max_length=1500)

    # Информация для доставки ниже не должна быть изменяема.
    delivery_method = serializers.CharField(read_only=True)
    delivery_status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Delivery
        fields = (
            'id',
            'order',
            'delivery_method',
            'delivery_status',
            'created_at',
            'updated_at',
            'courier',
            'notes'
        )


class DeliveryRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь детали доставки.

    Атрибуты:
        * 'delivery_status' (SerializerMethodField): метод получения статуса.
    """

    delivery_status = serializers.SerializerMethodField(method_name='get_status')

    class Meta:
        model = Delivery
        fields = (
            'id',
            'order',
            'delivery_method',
            'delivery_status',
            'created_at',
            'updated_at',
            'courier',
            'notes'
        )

    @staticmethod
    def get_status(instance: Delivery) -> str:
        """Получить статус."""
        readable_status = instance.get_readable_status(instance.delivery_status)
        return readable_status


class DeliveryDeleteSerializer(serializers.ModelSerializer):
    """
        Преобразователь удаления доставки.
    """

    class Meta:
        model = Delivery
        fields = (
            'id',
        )
