using System;
using SVH.FileService.Core.Enums;

namespace SVH.FileService.Core.Rabbit.Messages
{
    public class VideoConvertTaskMessage
    {
        public Guid FileId { get; set; }

        public VideoFormat Format { get; set; }
    }
}
