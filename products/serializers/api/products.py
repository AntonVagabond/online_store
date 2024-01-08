from rest_framework import serializers

from products.models.products import Product
from products.serializers.nested.categories import CategoryNestedSerializer
from products.serializers.nested import products
from products.serializers.nested.providers import ProviderNestedSerializer


class ProductSearchSerializer(serializers.ModelSerializer):
    """Преобразователь поиска товаров."""

    class Meta:
        model = Product
        fields = ('id', 'name')


class ProductListSerializer(serializers.ModelSerializer):
    """
    Преобразователь списка товаров.

    Аттрибуты:
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_images = products.ProductImagesNestedSerializer(many=True,
                                                            read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity', 'category', 'product_images')


class ProductRetrieveSerializer(serializers.ModelSerializer):
    """
    Преобразователь извлечения товара.

    Аттрибуты:
        * `category` (CategoryNestedSerializer): категория.
        * `provider` (ProviderNestedSerializer): поставщик.
        * `product_description` (ProductDescriptionNestedSerializer): описание товара.
        * `product_feature` (ProductFeatureNestedSerializer): хар-ки товара.
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    # region -------------------- АТРИБУТЫ ИЗВЛЕЧЕНИЯ ТОВАРА ------------------------
    category = CategoryNestedSerializer()
    provider = ProviderNestedSerializer()
    product_description = products.ProductDescriptionNestedSerializer()
    product_feature = products.ProductFeatureNestedSerializer()
    product_images = products.ProductImagesNestedSerializer()
    # endregion ---------------------------------------------------------------------

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'is_available',
            'price',
            'quantity',
            'category',
            'provider',
            'product_description',
            'product_feature',
            'product_images',
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Преобразователь создания товара.

    Аттрибуты:
        * `product_description` (ProductDescriptionNestedSerializer): описание товара.
        * `product_feature` (ProductFeatureNestedSerializer): хар-ки товара.
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_description = products.ProductDescriptionNestedSerializer()
    product_feature = products.ProductFeatureNestedSerializer()
    product_images = products.ProductImagesNestedSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'is_available',
            'price',
            'quantity',
            'product_description',
            'product_feature',
            'product_images',
        )


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Преобразователь обновления товара.

    Аттрибуты:
        * `product_description` (ProductDescriptionNestedSerializer): описание товара.
        * `product_feature` (ProductFeatureNestedSerializer): хар-ки товара.
        * `product_images` (ProductImagesNestedSerializer): изображение товара.
    """

    product_description = products.ProductDescriptionNestedSerializer()
    product_feature = products.ProductFeatureNestedSerializer()
    product_images = products.ProductImagesNestedSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'is_available',
            'price',
            'quantity',
            'product_description',
            'product_feature',
            'product_images',
        )
