import requests
from django.conf import settings
from svh.celery import app


def get_files():
    resp = requests.get('%s/api/Files?rescan=true' % (settings.FILESERVICE_URL,))
    if resp.status_code == 200:
        return resp.json()


def get_file_url(fileid):
    return '%s/api/Files/%s' % (settings.FILESERVICE_URL, fileid)


def start_conversion(fileid, format):
    with app.connection() as conn:
        with conn.channel() as channel:
            producer = app.amqp.Producer(channel)
            producer.publish(body={'FileId': fileid, 'Format': format},
                             exchange='fileservice.event.direct', routing_key='fileservice',
                             headers={'MessageType': 'VideoConvertTaskMessage'})



