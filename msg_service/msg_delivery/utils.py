import requests
from django.core.mail import send_mail
from django.conf import settings


class MsgSender():
    def __init__(self, user, message):
        self.__user = user
        self.__message = message

    def send_email(self):
        try:
            send_mail(
                subject='Уведомление',
                message=self.__message,
                from_email=settings.SENDER_EMAIL,
                recipient_list=[self.__user.email],
                fail_silently=False
            )
            return True
        except Exception:
            return False

    def send_sms(self):
        try:
            from twilio.rest import Client
            client = Client("ACCOUNT_SID", "AUTH_TOKEN")
            client.messages.create(
                body=self.__message,
                from_=settings.SENDER_NUMBER,
                to=self.__user.phone
            )
            return True
        except Exception:
            return False

    def send_telegram(self):
        try:
            requests.post(
                f'https://api.telegram.org/{settings.BOT_TOKEN}/sendMessage',
                json={'chat_id': self.__user.telegram_id, 'text': self.__message}
            )
            return True
        except Exception:
            return False