from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import UserCreateView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
]
