from __future__ import annotations

from typing import Union

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.management import call_command
from djoser import email as djoser_email

from config.celery import app

User = get_user_model()


# region --------------------------- REGISTRATION -----------------------------------
@app.task(bind=True, default_retry_delay=5 * 60)
def send_registration_task(
        self: send_registration_task,
        context: dict[str, Union[str, int]],
        email: list[str],
) -> None:
    """Задача на отправку электронного письма о создании пользователя."""
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.ActivationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
# endregion -------------------------------------------------------------------------


# region --------------------------- AUTHORISATION ----------------------------------
@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_task(
        self: send_reset_password_task,
        context: dict[str, Union[str, int]],
        email: list[str],
) -> None:
    """Задача на отправку электронного письма для нового пароля."""
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.PasswordResetEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task(bind=True, default_retry_delay=5 * 60)
def send_activation_task(
        self: send_activation_task,
        context: dict[str, Union[str, int]],
        email: list[str],
) -> None:
    """Задача на отправку электронного письма об активации пользователя."""
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.ActivationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_confirm_task(
        self: send_reset_password_confirm_task,
        context: dict[str, Union[str, int]],
        email: list[str]
) -> None:
    """
    Задача на отправку электронного письма о сбросе пароля
    и изменение его на новый.
    """
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.PasswordChangedConfirmationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
# endregion -------------------------------------------------------------------------


@shared_task()
def db_backup_task() -> None:
    """Выполнение резервного копирования базы данных."""
    call_command('dbackup')
