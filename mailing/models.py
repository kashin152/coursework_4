from django.db import models
from django.db.models import BooleanField


class Recipient(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(unique=True, verbose_name="Email получателя", help_text="Введите Email получателя")
    full_name = models.CharField(verbose_name="ФИО получателя", help_text="Введите ФИО получателя", unique=True)
    comment = models.TextField(max_length=150, null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]


class Message(models.Model):
    """Модель управление сообщениями"""
    tema_message = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(null=True, blank=True, help_text="Введите текст письма")

    def __str__(self):
        return self.tema_message

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["tema_message"]


class Mailing(models.Model):
    """Модель управление рассылками"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    recipient = models.ManyToManyField(Recipient, related_name="Получатели")

    date_first_message = models.DateField(auto_now_add=True, verbose_name="Дата и время первой отправки")
    date_end_message = models.DateField(auto_now=True, verbose_name="Дата и время окончания отправки")

    status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=True, default="created", verbose_name="Статус")

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
