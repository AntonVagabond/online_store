from django.db import models


class BaseModel(models.Model):
    """
    Абстрактная базовая модель. Нужна для инициализации objects в других моделях.
    """
    objects = models.Manager()

    class Meta:
        abstract = True
