from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
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
from mailing.servicies import (
    get_mailing_from_cache,
    get_message_from_cache,
    send_mailing,
)


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
            status="running",
        ).count()
        # Количество уникальных получателей
        context["unique_recipients_count"] = Recipient.objects.distinct().count()

        return context


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_create.html"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        # Автоматически присваиваем пользователя созданному получателю
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_create.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Recipient.DoesNotExist:
            raise PermissionDenied(
                "У Вас нет прав для редактирования этого получателя."
            )


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.has_perm("mailing.recipient_delete")
            or self.request.user.owner
        )

    def handle_no_permission(self):
        return redirect("mailing:recipient_list")


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "can_view_other_client"

        ):
            return Recipient.objects.all()
        else:
            user = self.request.user
            return Recipient.objects.filter(owner=user)


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        # Автоматически присваиваем пользователя созданному сообщению
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Message.DoesNotExist:
            raise PermissionDenied("У Вас нет прав для редактирования этого сообщения.")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.message.owner
            and self.request.user.has_perm("mailing.message_delete")
        )

    def handle_no_permission(self):
        return redirect("mailing:message_list")


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "can_view_other_message"
        ):
            return get_message_from_cache()
        else:
            user = self.request.user
            return Message.objects.filter(owner=user)


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "can_view_other_mailing"
        ):
            return get_mailing_from_cache()
        else:
            return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_create.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        # Автоматически присваиваем пользователя созданной рассылке
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Получаем стандартные аргументы формы
        kwargs = super().get_form_kwargs()
        # Добавляем текущего пользователя в аргументы
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_create.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Mailing.DoesNotExist:
            raise PermissionDenied("У Вас нет прав для редактирования этой рассылки.")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.has_perm("mailing.mailing_delete")
            or self.request.mailing.owner
        )

    def handle_no_permission(self):
        return redirect("mailing:mailing_list")

    def get_object(self, queryset=None):
        return get_object_or_404(Mailing, pk=self.kwargs["pk"])


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"


class SendMailingView(View):
    """Отправка и отключение сообщения/рассылки"""

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        response = send_mailing(mailing)
        return render(
            request, "mailing_detail.html", {"mailing": mailing, "response": response}
        )


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailing_attempt_list.html"
    context_object_name = "mailing_attempt_list"

    def get_queryset(self):
        """Проверка прав пользователя на просмотр попыток рассылки"""
        queryset = super().get_queryset()
        return queryset.filter(mailing__owner=self.request.user)

    def get_context_data(self, **kwargs):
        """Добавление переменных в шаблон страницы статистики"""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["attempts_count"] = queryset.count()
        context["attempts_success_count"] = queryset.filter(status="successful").count()
        context["attempts_error_count"] = queryset.filter(
            status="not_successful"
        ).count()
        return context

    # def get_queryset(self):
    #     """Фильтрация объектов по текущему пользователю"""
    #     return MailingAttempt.objects.filter(owner=self.request.user)
    #
    # def get_context_data(self, **kwargs):
    #     """Добавление переменных в шаблон страницы статистики"""
    #     context = super().get_context_data(**kwargs)
    #     # Получаем статистику по попыткам рассылок для текущего пользователя
    #     total_mailings, successful_mailings, failed_mailings = MailingAttempt.get_user_statistics(self.request.user)
    #
    #     # Обновляем контекст
    #     context["attempts_count"] = total_mailings
    #     context["attempts_success_count"] = successful_mailings
    #     context["attempts_error_count"] = failed_mailings
    #
    #     return context


class BlockMailingView(LoginRequiredMixin, View):

    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return render(request, "mailing_block.html", {"mailing": mailing})

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)

        if not request.user.has_perm("mailing.can_disable_mailings"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки.")

        # Переключение состояния блокировки
        mailing.is_blocked = not mailing.is_blocked

        if mailing.is_blocked:
            mailing.status = "blocked"
        else:
            if mailing.status == "blocked":
                mailing.status = "unblocked"

        mailing.save()
        return redirect("mailing:mailing_list")
