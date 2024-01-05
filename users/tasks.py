from typing import Union

from django.contrib.auth import get_user_model
from djoser import email as djoser_email

from config.celery import app

User = get_user_model()


@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_task(
        self,
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
        self,
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
        self,
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
