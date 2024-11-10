from config.settings import CACHE_ENABLED
from django.core.cache import cache
from mailing.models import Mailing, Message, Recipient, MailingAttempt
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from django.db.models import Q
from config.settings import EMAIL_HOST_USER


def get_mailing_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings


def get_message_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_recipient_from_cache():
    """Получает данные из кэша, если кэш пуст, получает данные из бд"""
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def send_mailing(mailing: Mailing = None):
    if not mailing:
        # Фильтруем рассылки по статусу и текущему времени
        mailings_to_send = Mailing.objects.filter(
            Q(status="created") | Q(status="completed") | Q(status="unblocked"),
            date_first_message__lte=timezone.now(),
        )
    else:
        mailings_to_send = [mailing]

    for mailing in mailings_to_send:
        # Меняем статус на "Запущена" перед началом отправки
        mailing.status = "running"
        mailing.start_datetime = timezone.now()
        mailing.save()

        success_count = 0

        for recipient in mailing.recipient.all():
            try:
                send_mail(
                    subject=mailing.message.theme_message,
                    message=mailing.message.text,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                )

                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="successfully",
                    mail_server_response="Письмо отправлено успешно.",
                    date_time_attempt=timezone.now(),
                )

                success_count += 1

            except BadHeaderError as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="not_successfully",
                    mail_server_response=str(e),
                    date_time_attempt=timezone.now(),
                )

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="not_successfully",
                    mail_server_response=str(e),
                    date_time_attempt=timezone.now(),
                )

        # Если все письма были отправлены успешно, меняем статус на "Завершена"
        if success_count == len(mailing.recipient.all()):
            mailing.status = "completed"
            mailing.end_datetime = timezone.now()
        mailing.save()
