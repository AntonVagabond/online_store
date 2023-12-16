from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from carts.service import Cart


@extend_schema_view(
    get=extend_schema(
        summary='Посмотреть корзину',
        tags=['Корзина'],
    ),
    post=extend_schema(
        summary='Добавить товар в корзину',
        tags=['Корзина'],
    ),
    patch=extend_schema(
        summary='Частично изменить корзину',
        tags=['Корзина'],
    ),
    delete=extend_schema(
        summary='Очистить корзину',
        tags=['Корзина'],
    ),
)
class CartAPIView(GenericAPIView):
    """Представление корзины."""

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request: Request) -> Response:
        cart = Cart(request)

        # Получаем список товаров из корзины и заносим их в словарь данных
        # для дальнейшего вывода ответа.
        product_list = {'product_list': list(cart.__iter__())}
        # Получаем общую сумму товаров из корзины.
        products_total_price = {'products_total_price': cart.get_total_price()}
        # Получаем общее кол-во товаров в корзине.
        product_count = {'product_count': cart.__len__()}
        cart_data = product_list | product_count | products_total_price
        return Response(cart_data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request: Request) -> Response:
        cart = Cart(request)

        # Добавляем товар, кол-во товара,
        # переопределение кол-ва товара (bool-значение), в корзину.
        data = request.data
        cart.add(
            product=data['product'],
            quantity=data['quantity'],
            update_quantity=data.get('update_quantity', False)
        )
        return Response(status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def patch(request: Request) -> Response:
        cart = Cart(request)
        product = request.data['product']
        # Удаляем товар из корзины, изменяя частично саму корзину.
        cart.remove(product)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request: Request) -> Response:
        cart = Cart(request)
        cart.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

