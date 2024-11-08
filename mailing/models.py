from django.db import models
from django.db.models import BooleanField
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone


class Recipient(models.Model):
    """Модель получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name="Email получателя")
    full_name = models.CharField(verbose_name="ФИО получателя", unique=True)
    comment = models.TextField(
        max_length=150, null=True, blank=True, verbose_name="Комментарий"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]


class Message(models.Model):
    """Модель управление сообщениями"""

    theme_message = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.theme_message

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["theme_message"]


class Mailing(models.Model):
    """Модель управление рассылками"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
        ("deactivated", "Отключена"),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient, related_name="Получатели")
    date_first_message = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время первой отправки"
    )
    date_end_message = models.DateTimeField(
        auto_now=True, verbose_name="Дата и время окончания отправки"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default="created",
        verbose_name="Статус",
    )

    # def send_mailing(self):
    #     if self.status != "created":
    #         return "Рассылка не может быть отправлена, так как статус не 'Создана'."
    #
    #     # Меняем статус на "Запущена" перед началом отправки
    #     self.status = "running"
    #     self.start_datetime = timezone.now()
    #     self.save()
    #
    #     success_count = 0
    #
    #     for recipient in self.recipient.all():
    #         try:
    #             send_mail(
    #                 subject=self.message.theme_message,
    #                 message=self.message.text,
    #                 from_email="from@example.com",
    #                 recipient_list=[recipient.email],
    #             )
    #
    #             MailingAttempt.objects.create(
    #                 mailing=self,
    #                 status="successfully",
    #                 mail_server_response="Письмо отправлено успешно.",
    #                 date_time_attempt=timezone.now(),
    #             )
    #
    #             success_count += 1
    #
    #         except BadHeaderError as e:
    #             MailingAttempt.objects.create(
    #                 mailing=self,
    #                 status="not_successfully",
    #                 mail_server_response=str(e),
    #                 date_time_attempt=timezone.now(),
    #             )
    #
    #         except Exception as e:
    #             MailingAttempt.objects.create(
    #                 mailing=self,
    #                 status="not_successfully",
    #                 mail_server_response=str(e),
    #                 date_time_attempt=timezone.now(),
    #             )
    #
    #     # Если все письма были отправлены успешно, меняем статус на "Завершена"
    #     if success_count == len(self.recipient.all()):
    #         self.status = "completed"
    #     self.save()
    #
    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["date_first_message", "message"]


def send_mailing_service():
    # Фильтруем рассылки по статусу "Создана" и текущему времени
    mailings_to_send = Mailing.objects.filter(status="created", date_first_message__lte=timezone.now())

    for mailing in mailings_to_send:
        try:
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
                        from_email="from@example.com",
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
            mailing.save()

        except Exception as e:
            # Логируем ошибку с самой рассылкой
            mailing.status = "error"
            mailing.save()
            # Здесь можно добавить логирование ошибки или уведомление администраторов
            print(f"Ошибка при отправке рассылки {mailing.id}: {str(e)}")


class MailingAttempt(models.Model):
    """Модель попытки рассылок"""

    STATUS_CHOICES = [
        ("successfully", "Успешно"),
        ("not_successfully", "Не успешно"),
    ]

    date_time_attempt = models.DateField(auto_now_add=True, verbose_name="Дата и время попытки"
    )

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        blank=True,
        default="created",
        verbose_name="Статус",
    )

    def formatted_date_time(self):
        return self.date_time_attempt.strftime("%d.%m.%Y %H:%M:%S")

    def __str__(self):
        return f"Попытка {self.id} - Статус: {self.status} в {self.date_time_attempt}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["date_time_attempt", "status"]
