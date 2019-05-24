import time
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

#allows method(log_time = {})
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logstr = '%r  %2.2f ms' % (method.__name__, (te - ts) * 1000)
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(logstr)
            for a in args:
                print(a)
            for a in kw:
                print(a)
        return result
    return timed

def add_types_in_context(request):
    return {'types': VideoFolder.objects.all_types()}