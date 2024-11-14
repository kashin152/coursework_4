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
        fields = ["theme_message", "text", "owner"]
        widgets = {
            "text": forms.Textarea(attrs={"placeholder": "Введите ваше сообщение..."}),
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["date_first_message", "date_end_message", "message", "recipient", "status"]
        widgets = {
            "date_first_message": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "date_end_message": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем получателей и сообщения по текущему пользователю
        self.fields['recipient'].queryset = Recipient.objects.filter(owner=user)
        self.fields['message'].queryset = Message.objects.filter(owner=user)
