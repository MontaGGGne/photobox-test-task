from celery import shared_task, group
from .models import User
from .utils import MsgSender


@shared_task(bind=True, max_retries=3)
def send_email_task(self, senders: MsgSender, user):
    if user.email:
        try:
            return senders.send_email(user.email)
        except Exception as e:
            self.retry(exc=e, countdown=3)

@shared_task(bind=True, max_retries=3)
def send_sms_task(self, senders: MsgSender, user):
    if user.phone:
        try:
            return senders.send_sms(user.phone)
        except Exception as e:
            self.retry(exc=e, countdown=10)

@shared_task(bind=True, max_retries=10)
def send_telegram_task(self, senders: MsgSender, user):
    if user.telegram_id:
        try:
            return senders.send_telegram(user.telegram_id)
        except Exception as e:
            self.retry(exc=e, countdown=10)

@shared_task
def dispatch_notifications(user_id, message):
    user = User.objects.get(id=user_id)
    senders = MsgSender(message)
    task_group = group(
        send_email_task.s(senders, user),
        send_sms_task.s(senders, user),
        send_telegram_task.s(senders, user)
    )

    result = task_group.apply_async()
    
    try:
        return result.get(timeout=60)
    except TimeoutError:
        return [False, False, False]