from django import forms

from mailing.models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    """Класс формы клиента"""

    class Meta:
        model = Recipient
        fields = ["full_name", "email", "comment"]


class MessageForm(forms.ModelForm):
    """Класс формы сообщения"""

    class Meta:
        model = Message
        fields = ["theme_message", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"placeholder": "Введите ваше сообщение..."}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "recipient"]  # Укажите поля для выбора

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].queryset = Message.objects.all()  # Все существующие сообщения
        self.fields["recipient"].queryset = Recipient.objects.all()  # Все существующие получатели
