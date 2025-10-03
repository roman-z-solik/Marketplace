from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class UserCreateView(CreateView):
    """Класс UserCreateView реализует функционал регистрации новых пользователей с
    дополнительной отправкой email-уведомления.
    Настройки email (settings.py):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' - это настройка Django,
    которая определяет механизм отправки электронной почты в приложении.
    EMAIL_HOST = 'smtp.******.ru'                - SMTP сервер почты, с которой отправляется
    письмо
    EMAIL_PORT = 587                             - порт
    EMAIL_USE_TLS = True                         - настройки TLS
    EMAIL_HOST_USER = 'your-email@*******.ru'    - email для авторизации на сервере почты,
    с которой отправляется письмо
    EMAIL_HOST_PASSWORD = 'your-password'        - пароль: ВНИМАНИЕ! нужен именно пароль
    приложения, а не почтового ящика!
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER         - настройка для отправки ошибок
    """

    model = CustomUser
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject=f"{user.first_name} {user.last_name}, вы зарегистрированы",
            message=f"{user.first_name} {user.last_name}, спасибо, что Вы "
            f"прошли регистрацию в нашем сервисе!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)
