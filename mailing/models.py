from django.db import models
from django.db.models import BooleanField
from django.core.mail import send_mail
from django.utils import timezone


class Recipient(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(unique=True, verbose_name="Email получателя")
    full_name = models.CharField(verbose_name="ФИО получателя", unique=True)
    comment = models.TextField(max_length=150, null=True, blank=True, verbose_name="Комментарий")

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
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Recipient, related_name="Получатели")
    date_first_message = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время первой отправки")
    date_end_message = models.DateTimeField(auto_now=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=True, default="created", verbose_name="Статус")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def send_mailing(self):
        if not self.is_active:
            return "Рассылка отключена."

        if self.status != "created":
            return "Рассылка уже запущена или завершена."

        self.status = "running"
        self.save()

        for recipient in self.recipient.all():
            send_mail(
                subject=self.message.theme_message,
                message=self.message.text,
                from_email='from@example.com',
                recipient_list=[recipient.email],
            )

        self.status = "completed"
        self.date_end_message = timezone.now()
        self.save()

    def reset_mailing(self):
        self.status = "created"
        self.is_active = True
        self.date_end_message = None
        self.save()

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["date_first_message", "message"]


class MailingAttempt(models.Model):
    """Модель попытки рассылок"""

    STATUS_CHOICES = [
        ("successfully", "Успешно"),
        ("not successfully", "Не успешно"),
    ]

    date_time_attempt = models.DateField(auto_now_add=True, verbose_name="Дата и время попытки")

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, blank=True, default="created", verbose_name="Статус")

    def __str__(self):
        return f"Попытка {self.id} - Статус: {self.status} в {self.date_time_attempt}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["date_time_attempt", "status"]
