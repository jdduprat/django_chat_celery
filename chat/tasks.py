from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime

# El decorador shared_task sirve para crear tareas independientes a la app.
# La tarea solo es una simulación tonta.
# Pero sabed que podéis usar cualquier librería y clase aquí. Incluido el orm para acceder a la bd.
@shared_task
def simulate_send_emails():
    #for i in range(1, num_emails):
    #    print('Sending email %d' % i);
        # esperamos un segundo.
    #    sleep(1)

    async_to_sync(get_channel_layer().group_send)("chat_123", {"type": "chat_message", "message":"Hora "})
    print("Hora ")

    return 'Emails sended'


