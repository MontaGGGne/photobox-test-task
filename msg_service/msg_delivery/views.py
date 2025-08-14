from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .celery_tasks import dispatch_notifications


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NotificationSendView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            message = request.data.get('message', '')
            
            if not message:
                return Response(
                    {'error': 'Message is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            dispatch_notifications.delay(user.id, message)
            return Response(
                {'status': 'Notification sent'},
                status=status.HTTP_202_ACCEPTED
            )
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )