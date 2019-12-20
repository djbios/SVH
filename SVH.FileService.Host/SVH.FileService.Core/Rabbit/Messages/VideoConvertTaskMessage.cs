using System;
using System.Collections.Generic;
using SVH.FileService.Common.Enums;

namespace SVH.FileService.Core.Rabbit.Messages
{
    public class VideoConvertTaskMessage : MessageBase
    {
        public Guid FileId { get; set; }

        public VideoFormat Format { get; set; }

        public Dictionary<string, object> Data { get; set; }

        public override string TargetEndpoint => "Tasks";
    }
}
