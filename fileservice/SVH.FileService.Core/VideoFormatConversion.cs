using System;
using SVH.FileService.Common.Enums;
using Xabe.FFmpeg.Enums;
using Xabe.FFmpeg.Streams;

namespace SVH.FileService.Core
{
    public static class VideoFormatConversion
    {
        public static IVideoStream SetFormat(this IVideoStream stream, VideoFormat format)
        {
            switch (format)
            {
                case VideoFormat.h264x1080p:
                    return stream.SetSize(VideoSize.Hd1080).SetCodec(VideoCodec.H264);
                case VideoFormat.h264x480p:
                    return stream.SetSize(VideoSize.Hd480).SetCodec(VideoCodec.H264);
                case VideoFormat.h264x720p:
                    return stream.SetSize(VideoSize.Hd720).SetCodec(VideoCodec.H264);
            }
            throw new ArgumentOutOfRangeException(nameof(format));
        }
    }
}
