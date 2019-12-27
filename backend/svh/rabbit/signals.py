import json

import django.dispatch
from celery import bootsteps
from django.conf import settings
from kombu import Consumer, Queue, Exchange

video_converted_signal = django.dispatch.Signal(providing_args=['source_file_id', 'result_file_id', 'format'])
synchronized_signal = django.dispatch.Signal()


class EventConsumerStep(bootsteps.ConsumerStep):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def get_consumers(self, channel):
        ep = settings.RABBIT_SETTINGS['RabbitEndpoints']['Events']
        ep_tasks = settings.RABBIT_SETTINGS['RabbitEndpoints']['Tasks']
        event_queue = Queue(ep['Queue'],
                            Exchange(name=ep['Exchange'],
                                     type=ep['ExchangeType'],
                                     durable=False),
                            ep['RoutingKey'])
        task_queue = Queue(ep_tasks['Queue'],
                           Exchange(name=ep_tasks['Exchange'],
                                    type=ep_tasks['ExchangeType'],
                                    durable=False),
                           ep_tasks['RoutingKey'])
        return [Consumer(channel,
                         queues=[event_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    @staticmethod
    def handle_message(body, message):
        data = json.loads(body)
        if message.headers['MessageType'] == 'VideoConvertedEventMessage':
            video_converted_signal.send(sender='rabbit',
                                        source_file_id=data["SourceId"],
                                        result_file_id=data["ResultId"],
                                        format=data["Format"])

        elif message.headers['MessageType'] == 'SynchronizedEventMessage':
            synchronized_signal.send('rabbit')

        else:
            print('Received message: {0!r}, {1!r}'.format(body, message.headers))
        message.ack()
