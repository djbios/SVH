import requests
from django.conf import settings
from svh.celery import app
from svh.rabbit.messages import send_message, VideoConvertTaskMessage


def get_files():
    url = '%s/api/Files?rescan=false' % (settings.FILESERVICE_URL,)
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()


def get_file_url(fileid):
    return '%s/api/Files/%s' % (settings.FILESERVICE_URL, fileid)


def start_conversion(fileId, format):
    send_message(VideoConvertTaskMessage(file_id=fileId, format=format))



