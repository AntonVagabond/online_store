from rest_framework import serializers

from carts.models.couriers import Courier


class CourierSearchSerializer(serializers.ModelSerializer):
    """Сериализатор поиска курьера."""

    class Meta:
        model = Courier
        fields = ('id', 'name', 'vehicle_type', 'is_available')


class CourierListSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка курьера.

    Аттрибуты:
        * `products` (ProductNestedSerializer): товары поставщика.
    """

    class Meta:
        model = Courier
        fields = ('id', 'name', 'vehicle_type', 'is_available')


class CourierRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор извлечения курьера.

    Аттрибуты:
        * `products` (ProductNestedSerializer): товары поставщика.
    """

    class Meta:
        model = Courier
        fields = (
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'vehicle_type',
            'is_available',
        )


class CourierCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания курьера."""

    class Meta:
        model = Courier
        fields = (
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'vehicle_type',
            'is_available',
        )


class CourierUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления курьера."""

    class Meta:
        model = Courier
        fields = (
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'vehicle_type',
            'is_available',
        )
