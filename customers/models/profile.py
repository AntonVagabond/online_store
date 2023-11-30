from django.core.cache import cache
from django.db import models
from django.utils import timezone

from common.models.mixins import BaseModel


class Profile(BaseModel):
    """Профиль покупателя"""

    customer = models.OneToOneField(
        to='customers.Customer',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Профиль',
        primary_key=True,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='customers/%Y/%m/%d',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'

    def __str__(self):
        return f'{self.customer} ({self.pk})'

    def is_online(self) -> bool:
        """Проверка покупателя на онлайн в течении последних 5 мин."""
        last_seen = cache.get(f'last-seen-{self.customer.id}')
        return bool(last_seen and timezone.timedelta(seconds=300))
