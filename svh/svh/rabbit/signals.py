import django.dispatch

video_converted_signal = django.dispatch.Signal(providing_args=['source_file_id', 'result_file_id', 'format'])

synchronized_signal = django.dispatch.Signal()
