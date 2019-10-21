# import pika
# from celery import bootsteps
# from django.conf import settings
# from kombu import Consumer
#
# from svh.rabbit.messages import MessageBase
# import django.dispatch
#
# conf = settings.RABBIT_SETTINGS
#
#
# def _get_connection_():
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host=conf['Host'],
#                                   port=conf['Port'],
#                                   credentials=pika.PlainCredentials(username=conf['UserName'],
#                                                                password=conf['Password']),
#                                   virtual_host=conf['VirtualHost']))
#     return connection
#
#
# video_converted_signal = django.dispatch.Signal(providing_args=['file_id'])
# synchronized_signal = django.dispatch.Signal()
#
#
# class RabbitConsumer:
#     def __init__(self):
#         connection = _get_connection_()
#         channel = connection.channel()
#         for endpoint in conf['RabbitEndpoints'].values():  # Initialize exchanges
#             channel.exchange_declare(exchange=endpoint['Exchange'], exchange_type=endpoint['ExchangeType'])
#
#         events_queue_name = conf['RabbitEndpoints']['Events']['Queue']
#         channel.queue_declare(queue=events_queue_name, exclusive=True)
#         channel.queue_bind(exchange=conf['RabbitEndpoints']['Events']['Exchange'],
#                            queue=events_queue_name)
#         channel.basic_consume(
#             queue=events_queue_name,
#             on_message_callback=self.callback
#         )
#         channel.start_consuming()
#
#     @staticmethod
#     def callback(ch, method, properties, body):
#         print(body)
#
#
# #rabbit_consumer = RabbitConsumer()
#
#
# def send_message(message: MessageBase):
#     connection = _get_connection_()
#     channel = connection.channel()
#     exchange = conf['RabbitEndpoints'][message.target_endpoint]['Exchange']
#     routing_key = conf['RabbitEndpoints'][message.target_endpoint]['RoutingKey']
#     channel.basic_publish(exchange=exchange,
#                           routing_key=routing_key,
#                           body=message.get_serialized(),
#                           properties=pika.BasicProperties(
#                               headers={'MessageType': message.__class__.__name__})
#                           )
#     connection.close()
#
#
