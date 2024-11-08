from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView, email_verification

app_name = "users"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
]
