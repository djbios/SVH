import requests
from django.conf import settings


def get_files():
    resp = requests.get('%s/api/Files' % (settings.FILESERVICE_URL,))
    if resp.status_code == 200:
        return resp.json()