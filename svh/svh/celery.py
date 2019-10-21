from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, bootsteps

# set the default Django settings module for the 'celery' program.
from django.conf import settings
from kombu import Consumer, Queue, Exchange

from svh.rabbit.messages import MessageBase
from svh.rabbit.signals import video_converted_signal, synchronized_signal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'svh.settings')

app = Celery('svh')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


conf = settings.RABBIT_SETTINGS


class EventConsumerStep(bootsteps.ConsumerStep):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def get_consumers(self, channel):
        ep = conf['RabbitEndpoints']['Events']
        event_queue = Queue(ep['Queue'],
                            Exchange(name=ep['Exchange'],
                                     type=ep['ExchangeType'],
                                     durable=False),
                            ep['RoutingKey'])
        return [Consumer(channel,
                         queues=[event_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    @staticmethod
    def handle_message(body, message):
        if message.headers['MessageType'] == 'VideoConvertedEventMessage':
            video_converted_signal.send(source_file_id=message["SourceId"],
                                        result_file_id=message["ResultId"],
                                        format=message["Format"])

        elif message.headers['MessageType'] == 'SynchronizedEventMessage':
            synchronized_signal.send('rabbit')

        else:
            print('Received message: {0!r}, {1!r}'.format(body, message.headers))
        message.ack()


app.steps['consumer'].add(EventConsumerStep)


def send_message(message: MessageBase):
    with app.producer_or_acquire() as producer:
        producer.publish(
            message.get_serialized(),
            #serializer='json',
            exchange=conf['RabbitEndpoints'][message.target_endpoint]['Exchange'],
            routing_key=conf['RabbitEndpoints'][message.target_endpoint]['RoutingKey'],
            #declare=[my_queue],
            retry=True,
            headers={'MessageType': message.__class__.__name__}
        )
pass