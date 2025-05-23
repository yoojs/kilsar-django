from celery import shared_task
from django.core.mail import send_mail
from django.db.transaction import on_commit
from django.conf import settings

@shared_task(name='todolist.tasks.send_mail_task')
def send_mail_task(subject, message, recipient_list):
    return send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )