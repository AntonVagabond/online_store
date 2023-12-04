from django.contrib import admin
from django.utils.safestring import mark_safe


class ModelaAdminWithImage(admin.ModelAdmin):
    @admin.display(description='Изображение', ordering='image')
    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return 'Нет изображения'
