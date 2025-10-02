from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject=f"{user.first_name} {user.last_name}, вы зарегистрированы",
            message=f"{user.first_name} {user.last_name}, спасибо, что Вы "
                    f"прошли регистрацию в нашем сервисе!",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)