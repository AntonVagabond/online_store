import os

from celery import Celery

# Установите модуль настроек Django по умолчанию для программы "celery".
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')

app = Celery('config')

# Использование строки здесь означает, что работнику не нужно сериализовывать
# объект конфигурации дочерним процессам.
# - пространство имен='CELERY' означает, что все ключи конфигурации, связанные с
# celery должны иметь префикс `CELERY_`.
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

# Загружайте модули задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
