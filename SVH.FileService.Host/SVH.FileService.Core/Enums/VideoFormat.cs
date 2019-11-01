using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace SVH.FileService.Core.Enums
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum VideoFormat
    {
        preview, gif, h264x480p, h264x1080p, h264x720p
    }
}
