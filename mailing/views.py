from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, MailingAttempt


class MailingHomeView(ListView):
    model = Mailing
    template_name = "home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Количество всех рассылок
        context["all_mailings_count"] = Mailing.objects.count()
        # Количество активных рассылок
        context["active_mailings_count"] = Mailing.objects.filter(
            status="running"
        ).count()
        # Количество уникальных получателей
        context["unique_recipients_count"] = Recipient.objects.distinct().count()

        return context


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_create.html"
    success_url = reverse_lazy("mailing:home")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_create.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = reverse_lazy("mailing:home")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_create.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_create.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"


class SendMailingView(View):
    """Отправка и отключение сообщения/рассылки"""

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        response = mailing.send_mailing()
        return render(
            request, "mailing_detail.html", {"mailing": mailing, "response": response}
        )

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Отключаем рассылку
        mailing.is_active = False  # Отключаем рассылку
        mailing.status = "deactivated"  # Меняем статус на "Отключена"
        mailing.date_end_message = timezone.now()  # Устанавливаем дату окончания
        mailing.save()

        return render(
            request,
            "mailing_detail.html",
            {"mailing": mailing, "message": "Рассылка отключена."},
        )


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailing_attempt_list.html"
    context_object_name = "mailing_attempt_list"

    def get_context_data(self, **kwargs):
        """Добавление переменных в шаблон страницы статистики"""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["attempts_count"] = queryset.count()
        context["attempts_success_count"] = queryset.filter(status="successfully").count()
        context["attempts_error_count"] = queryset.filter(status="not_successfully").count()
        return context


