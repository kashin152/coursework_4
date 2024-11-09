from django.contrib import admin
from mailing.models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    list_filter = ("full_name",)
    search_fields = (
        "email",
        "full_name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme_message", "text")
    list_filter = ("theme_message",)
    search_fields = (
        "theme_message",
        "text",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_first_message",
        "date_end_message",
        "status",
        "message",
    )
    list_filter = ("status",)
    search_fields = (
        "message",
        "recipient",
    )


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "date_time_attempt", "status", "mail_server_response", "mailing")
    list_filter = (
        "status",
        "date_time_attempt",
    )
    search_fields = ("date_time_attempt",)