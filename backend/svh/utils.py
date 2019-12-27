import time
from svh.models import VideoFile, VideoFolder
from django.conf import settings


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


def log_exception(method):
    def logged(*args, **kw):
        try:
            result = method(*args, **kw)
            return result
        except Exception as e:
            print(e)

    return logged

def common_context_variables(request):
    return {
        'types': VideoFolder.objects.all_types(),
        'metrika': settings.METRICS_SCRIPT
    }