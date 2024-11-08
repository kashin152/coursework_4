from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
import secrets

from .models import CustomsUser
from django.shortcuts import render, get_object_or_404, redirect

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = CustomsUser
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        # Сохраняем пользователя только если форма валидна
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

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
    return redirect(request("users:login"))

