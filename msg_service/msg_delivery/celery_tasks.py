from __future__ import absolute_import, unicode_literals

from celery import shared_task, group
from .models import User
from .utils import MsgSender


@shared_task(bind=True, max_retries=3)
def send_email_task(self, user_id, message):
    senders = MsgSender(user_id, message)
    user = User.objects.get(id=user_id)
    if user.email:
        try:
            return senders.send_email(user, message)
        except Exception as e:
            self.retry(exc=e, countdown=3)

@shared_task(bind=True, max_retries=3)
def send_sms_task(self, user_id, message):
    senders = MsgSender(user_id, message)
    user = User.objects.get(id=user_id)
    if user.phone:
        try:
            return senders.send_sms(user, message)
        except Exception as e:
            self.retry(exc=e, countdown=10)

@shared_task(bind=True, max_retries=10)
def send_telegram_task(self, user_id, message):
    senders = MsgSender(user_id, message)
    user = User.objects.get(id=user_id)
    if user.telegram_id:
        try:
            return senders.send_telegram(user, message)
        except Exception as e:
            self.retry(exc=e, countdown=10)

@shared_task
def dispatch_notifications(user_id, message):
    task_group = group(
        send_email_task.s(user_id, message),
        send_sms_task.s(user_id, message),
        send_telegram_task.s(user_id, message)
    )

    result = task_group.apply_async()
    
    try:
        return result.get(timeout=60)
    except TimeoutError:
        return [False, False, False]