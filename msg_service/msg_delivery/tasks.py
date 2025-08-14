from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import User
from .utils import MsgSender


@shared_task(bind=True, max_retries=3)
def send_notification(self, user_id, message):
    user = User.objects.get(id=user_id)
    sender = MsgSender(user=user, message=message)
    
    if user.email and sender.send_email():
        return
    elif user.phone and sender.send_sms():
        return
    elif user.telegram_id and sender.send_telegram():
        return
    
    self.retry(countdown=60)