from rest_framework import serializers

from delivers.models.couriers import Vehicle


class VehicleRetrieveSerializer(serializers.ModelSerializer):
    """
        Преобразователь детали транспорта.
    """

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'name',
        )


class VehicleCreateSerializer(serializers.ModelSerializer):
    """
        Преобразователь создания транспорта.

        Атрибуты:
            * `name` (CharField): поле названия транспорта.

    """
    name = serializers.CharField(max_length=40)

    class Meta:
        model = Vehicle
        fields = (
            'id',
            'name',
        )


class VehicleDeleteSerializer(serializers.ModelSerializer):
    """
        Преобразователь удаления транспорта.
    """

    class Meta:
        model = Vehicle
        fields = (
            'id',
        )
