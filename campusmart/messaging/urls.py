# messaging/urls.py

from django.urls import path
from .views import send_message, inbox, message_detail

app_name = 'messaging'

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('send/<int:recipient_id>/', send_message, name='send_message'),
    path('message/<int:message_id>/', message_detail, name='message_detail'),
]

