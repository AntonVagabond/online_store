from carts.models.carts import Cart
from carts.models.orders import Order
from carts.models.payments import OrderPayment
from users.models.users import User


class _PaymentAmountService:
    """
    Компонентный класс.
    Сервисная часть для суммы оплаты.
    """
    def __init__(
            self,
            user: User,
            order: Order,
            payment_data: dict[str, str],
    ) -> None:
        self._user = user
        self._order = order
        self.__payment_data = payment_data

    def __get_cart_current_user(self) -> Cart:
        """Получить корзину текущего пользователя."""
        return Cart.objects.filter(user=self._user).first()

    @staticmethod
    def __get_cart_price(cart: Cart) -> str:
        """Получить сумму заказа."""
        return Cart.objects.get_cart_price(cart)

    def __add_payment_amount(self, price: str):
        """Добавление суммы оплаты в данные оплаты."""
        self.__payment_data.update(payment_amount=price)

    def __add_payment_creation_time(self):
        """Добавление времени у создания оплаты."""
        date = self._order.order_date
        additional_data = {key: date for key in ('created_at', 'update_at')}
        self.__payment_data |= additional_data

    def __create_payment(self) -> None:
        """Создание оплаты."""
        OrderPayment.objects.create(order_id=self._order.pk, **self.__payment_data)

    def execute_add_amount(self) -> None:
        """Выполнить добавление суммы оплаты заказа."""
        cart = self.__get_cart_current_user()
        price = self.__get_cart_price(cart)
        self.__add_payment_amount(price)
        self.__add_payment_creation_time()
        self.__create_payment()
