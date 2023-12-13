from django.db import models
from rest_framework.authtoken.models import Token


class BaseModel(models.Model):
    """
    Абстрактная базовая модель. Нужна для инициализации objects в других моделях.
    """
    objects = models.Manager()

    class Meta:
        abstract = True


class CustomToken(BaseModel, Token):
    """
    Абстрактная модель Токена. Нужна для инициализации objects.
    """
    class Meta:
        abstract = True
