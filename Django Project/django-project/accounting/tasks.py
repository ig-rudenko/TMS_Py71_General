from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@shared_task
def hello_world():
    print("hello world")


@shared_task(queue="email", rate_limit="100/m")
def welcome_email_sender(user_id: int, app_name: str = "test") -> str:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "user does not exist"

    if not user.email:
        return "required email address"

    text = f"Спасибо, что зарегистрировались в приложении {app_name}"
    subject = f"Welcome to {app_name}"

    send_mail(subject, text, settings.EMAIL_HOST_USER, [user.email])

    return "success"
