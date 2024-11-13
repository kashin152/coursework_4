from django.db import models
from users.models import CustomsUser


class Recipient(models.Model):
    """Модель получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name="Email получателя")
    full_name = models.CharField(verbose_name="ФИО получателя", unique=True)
    comment = models.TextField(
        max_length=150, null=True, blank=True, verbose_name="Комментарий"
    )
    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]
        permissions = [("can_view_other_client", "Может просматривать чужих клиентов")]


class Message(models.Model):
    """Модель управление сообщениями"""

    theme_message = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.theme_message

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["theme_message"]
        permissions = [
            ("can_view_other_message", "Может просматривать чужие сообщения")
        ]


class Mailing(models.Model):
    """Модель управление рассылками"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("completed", "Завершена"),
        ("blocked", "Заблокирована"),
        ("unblocked", "Разблокирована"),
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
    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"Рассылка для сообщения: «{self.message}»"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["date_first_message", "message"]
        permissions = [
            ("can_view_other_mailing", "Может просматривать чужие рассылки"),
            ("can_mailing_blocked", "Может блокировать рассылки"),
        ]


class MailingAttempt(models.Model):
    """Модель попытки рассылок"""

    STATUS_CHOICES = [
        ("successfully", "Успешно"),
        ("not_successfully", "Не успешно"),
    ]

    date_time_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        blank=True,
        default="not_successfully",
        verbose_name="Статус",
    )
    owner = models.ForeignKey(
        CustomsUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def formatted_date_time(self):
        return self.date_time_attempt.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Попытка {self.id} - Статус: {self.status} в {self.date_time_attempt}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["date_time_attempt"]
