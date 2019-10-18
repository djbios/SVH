using System;
using SVH.FileService.Core.Enums;

namespace SVH.FileService.Core.Rabbit.Messages
{
    public class VideoConvertTaskMessage : MessageBase
    {
        public Guid FileId { get; set; }

        public VideoFormat Format { get; set; }

        public override string TargetEndpoint => "Tasks";
    }
}
