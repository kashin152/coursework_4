from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.core.mail import send_mail
import secrets
from django.http import HttpResponseForbidden
from .models import CustomsUser
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = CustomsUser
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # Сохраняем пользователя только если форма валидна
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"

        # Отправляем письмо с подтверждением почты
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылки для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(CustomsUser, token=token)
    user.is_active = True
    user.save()
    return redirect("users:login")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomsUser
    form_class = CustomUserUpdateForm
    template_name = "register.html"
    success_url = reverse_lazy("users:user_list")


class UserListView(ListView):
    model = CustomsUser
    template_name = "user_list.html"
    context_object_name = "user_list"

    def get_queryset(self):
        return CustomsUser.objects.all()


class UserDetailView(DetailView):
    model = CustomsUser
    template_name = "user_profile.html"
    context_object_name = "user_profile"


class BlockUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomsUser, id=user_id)
        if not request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки.")
        return render(request, "user_block.html", {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(CustomsUser, id=user_id)

        if not request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")

        # Изменяем состояние блокировки
        user.is_blocked = not user.is_blocked
        user.save()

        return redirect("users:user_list")
