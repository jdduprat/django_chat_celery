# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from datetime import datetime

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


from django.http import HttpResponse
from chat.tasks import simulate_send_emails

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Vista que llama a la tarea.
def send_emails(request):
    simulate_send_emails.delay(10)
    return HttpResponse('Emails sended using Celery') 


def envia_al_socket():
    async_to_sync(get_channel_layer().group_send)("chat_123", {"type": "chat_message", "message":"Hora "+ datetime.now().time})
    print("Hora "+ datetime.now().time)
