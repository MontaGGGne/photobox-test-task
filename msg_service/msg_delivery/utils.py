import requests
import logging
from django.core.mail import EmailMessage
from django.conf import settings
from twilio.rest import Client


logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class MsgSender():
    def __init__(self, user, message):
        self.__user = user
        self.__message = message

    def send_email(self):
        try:
            email = EmailMessage(subject='Уведомление',
                                 body=self.__message,
                                 to=[self.__user.email])
            email.send()
            return True
        except Exception as e:
            logging.error(f"Fail send email: {repr(e)}")
            return False

    def send_sms(self):
        try:
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID,
                                   settings.TWILIO_AUTH_TOKEN)
            twilio_client.messages.create(
                body=self.__message,
                from_=settings.SENDER_NUMBER,
                to=self.__user.phone
            )
            return True
        except Exception as e:
            logging.error(f"Fail send sms: {repr(e)}")
            return False

    def send_telegram(self):
        try:
            requests.get(
                f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage',
                json={'chat_id': self.__user.telegram_id, 'text': self.__message}
            )
            return True
        except Exception as e:
            logging.error(f"Fail send telegram: {repr(e)}")
            return False