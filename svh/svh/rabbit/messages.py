import json
from django.conf import settings
from svh.celery import app


class MessageBase:
    target_endpoint = ''
    _data = {}

    def get_serialized(self):
        return json.dumps(self._data)


class VideoConvertTaskMessage(MessageBase):
    target_endpoint = 'Tasks'

    def __init__(self, file_id, format):
        self._data = {
            'FileId': file_id,
            'Format': format
        }


def send_message(message: MessageBase):
    with app.producer_or_acquire() as producer:
        producer.publish(
            message.get_serialized(),
            exchange=settings.RABBIT_SETTINGS['RabbitEndpoints'][message.target_endpoint]['Exchange'],
            routing_key=settings.RABBIT_SETTINGS['RabbitEndpoints'][message.target_endpoint]['RoutingKey'],
            retry=True,
            headers={'MessageType': message.__class__.__name__},
        )
