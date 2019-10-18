using System;
using SVH.FileService.Core.Enums;

namespace SVH.FileService.Core.Rabbit.Messages
{
    public class VideoConvertedEventMessage : MessageBase
    {
        public Guid SourceId { get; set; }

        public Guid ResultId { get; set; }

        public VideoFormat Format { get; set; }

        public override string TargetEndpoint => "Events";
    }
}
