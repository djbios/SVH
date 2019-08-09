import ffmpeg
from svh.models import VIDEO_FORMATS
from svh.utils import timeit


@timeit
def convert_video_to_format(input_path, output_path, format):
    stream = ffmpeg.input(input_path)
    format_args = dict(VIDEO_FORMATS)[format] # todo another formats here
    stream = stream.output(stream, output_path, vcodec='libx264')
    print([output_path, input_path])
    stream.run()

