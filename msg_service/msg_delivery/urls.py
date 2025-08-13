from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('send/', NotificationView.as_view(), name='send'),
]