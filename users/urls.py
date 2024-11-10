from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView, email_verification, UserListView, BlockUserView, UserUpdateView, UserDetailView

app_name = "users"


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("user_block/<int:user_id>", BlockUserView.as_view(), name="user_block"),
    path("user_update/<int:pk>", UserUpdateView.as_view(), name="user_update"),
    path("user_profile/<int:pk>", UserDetailView.as_view(), name="user_profile"),
]
