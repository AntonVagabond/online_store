from __future__ import annotations

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


@shared_task()
def db_backup_task() -> None:
    """Выполнение резервного копирования базы данных."""
    call_command('dbackup')
