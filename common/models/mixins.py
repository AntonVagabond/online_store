from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BaseModel(models.Model):
    """
    Абстрактная базовая модель. Нужна для инициализации objects в других моделях.
    """
    objects = models.Manager()

    class Meta:
        abstract = True


class DateMixin(BaseModel):
    """Абстрактная модель даты и времени"""

    created_at = models.DateTimeField(
        verbose_name='Создан в',
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен в',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        """Сохраняем информацию о создании и обновлении."""

        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin):
    """Абстрактная модель информации"""

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',
        verbose_name='Созданный',
        null=True,
    )
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Обновленный',
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        user = get_current_user()

        if user and not user.pk:
            user = None

        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)
