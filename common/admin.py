from typing import Union

from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from products.models.categories import Category


class ModelaAdminWithImage(admin.ModelAdmin):
    """Общая модель админа для отображения ссылок изображения."""

    @admin.display(description='Изображение', ordering='image')
    def image_show(self, obj: type[Category]) -> Union[str, SafeString]:
        """Отображает изображение."""

        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return 'Нет изображения'
