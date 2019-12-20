using System;

namespace SVH.FileService.Core.Models
{
    public class FileDto
    {
        public Guid FileId { get; set; }

        public string FileName { get; set; }

        public DateTimeOffset UploadDate { get; set; }
    }
}
