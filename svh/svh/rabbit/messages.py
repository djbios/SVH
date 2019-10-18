import json


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