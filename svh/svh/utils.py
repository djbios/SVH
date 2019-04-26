import os

from django.conf import settings
from twisted.internet import protocol, defer
from crochet import setup
from svh.models import VideoFile, VideoFolder

setup()

class Protocol(protocol.ProcessProtocol):
    logs = []

    def __init__(self):
        self.deferred = defer.Deferred()

    def errReceived(self, data):
        self.logs.append(str(data))

    def processEnded(self, reason):
        self.deferred.callback({'code':reason.value.exitCode, 'logs':self.logs})
