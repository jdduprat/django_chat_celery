from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chat.tasks import simulate_send_emails

# Establecer las opciones de django para la aplicación de celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Crear la aplicación de Celery
app = Celery('chat')

# Especificamos que las variables de configuración de Celery se encuentran
# en el fichero `settings.py` de Django.
# El parámetro namespace es para decir que las variables de configuración de
# Celery en el fichero settings empiezan por el prefijo *CELERY_*
app.config_from_object('django.conf:settings', namespace='CELERY')

# Este método auto-registra las tareas para el broker. 
# Busca tareas dentro de todos los archivos `tasks.py` que haya en las apps
# y las envía a Redis automáticamente.
app.autodiscover_tasks()


# Configuramos la zona horaria para que las tareas se ejecuten a la hora correcta.
app.conf.timezone = 'America/Argentina/Buenos_Aires'

''' # Decorador para añadir configuración extra después de conectarse.
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print('sdf')
    async_to_sync(get_channel_layer().group_send)("chat_123", {"type": "chat_message", "message":"me conecte"})
    # Ejecuta la tarea test('hello') cada 10 segundos
    #sender.add_periodic_task(1.0, test.s('hello'), name='add every 1')


    sender.add_periodic_task(10.0, mensaje.s('10'), name='socket asd')

    # Ejecuta la tarea test('world') cada 10 segundos
    #sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Ejecuta la tarea cada lunes a las 7:30 am
    #sender.add_periodic_task(
    #    crontab(hour=7, minute=30, day_of_week=1),
    #    test.s('Happy Mondays!'),
    #)
 '''
@app.task
def test(arg):
    print(arg)


@app.task
def mensaje(arg):
    async_to_sync(get_channel_layer().group_send)("chat_123", {"type": "chat_message", "message":"Hola a cada rato"},immediately=True)

''' 
app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'chat.celery.mensaje',
        'schedule': 5.0,
        'args': ('10',)
    },
} ''' 


# Other Celery settings
#CELERY_BEAT_SCHEDULE = {
#    'task-number-one': {
#        'task': 'chat.celery.test',
#        'schedule': 1,
#        'args': ("holaaaaaaaaaaaaa",)
#    },
#}