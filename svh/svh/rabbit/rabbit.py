import pika
from django.conf import settings
from svh.rabbit.messages import MessageBase

conf = settings.RABBIT_SETTINGS


def _get_connection_():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=conf['Host'],
                                  port=conf['Port'],
                                  credentials=pika.PlainCredentials(username=conf['UserName'],
                                                               password=conf['Password']),
                                  virtual_host=conf['VirtualHost']))
    return connection


class RabbitConsumer:
    def __init__(self):
        connection = _get_connection_()
        channel = connection.channel()
        for endpoint in conf['RabbitEndpoints'].values():  # Initialize exchanges
            channel.exchange_declare(exchange=endpoint['Exchange'], exchange_type=endpoint['ExchangeType'])


rabbit_consumer = RabbitConsumer()


def send_message(message: MessageBase):
    connection = _get_connection_()
    channel = connection.channel()
    exchange = conf['RabbitEndpoints'][message.target_endpoint]['Exchange']
    routing_key = conf['RabbitEndpoints'][message.target_endpoint]['RoutingKey']
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message.get_serialized(),
                          properties=pika.BasicProperties(
                              headers={'MessageType': message.__class__.__name__})
                          )
    connection.close()

pass