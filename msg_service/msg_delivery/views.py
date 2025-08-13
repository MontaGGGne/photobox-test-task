from django.shortcuts import render

from rest_framework import generics
from .models import User
from .celery_tasks import dispatch_notifications

class NotificationView(generics.CreateAPIView):
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        dispatch_notifications.delay(user.id, "Важное уведомление!")
