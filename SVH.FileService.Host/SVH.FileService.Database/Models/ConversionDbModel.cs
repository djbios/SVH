using SVH.FileService.Common.Enums;

namespace SVH.FileService.Database.Models
{
    public class ConversionDbModel
    {
        public long Id { get; private set; }

        public FileDbModel Source { get; set; }

        public FileDbModel Result { get; set; }

        public VideoFormat VideoFormat { get; set; }

        public long Tryes { get; set; } 

        public ConversionStatus Status { get; set; }
    }
}
