from django.core.cache import cache
from django.db import models
from django.utils import timezone

from common.models.base import BaseModel


class Profile(BaseModel):
    """Профиль покупателя"""

    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
        primary_key=True,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='users/%Y/%m/%d',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self) -> str:
        return f'{self.user} ({self.pk})'

    def is_online(self) -> bool:
        """Проверка пользователя на онлайн в течении последних 5 мин."""
        last_seen = cache.get(f'last-seen-{self.user.id}')
        return bool(last_seen and timezone.timedelta(seconds=300))
