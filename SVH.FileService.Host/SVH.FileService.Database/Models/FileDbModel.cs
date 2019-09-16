using System;

namespace SVH.FileService.Database.Models
{
    public class FileDbModel
    {
        public FileDbModel(string fileName)
        {
            FileName = fileName;
            FileId = Guid.NewGuid();
            UploadDate = DateTimeOffset.Now;
        }

        public long Id { get; private set; }

        public Guid FileId { get; set; }

        public string FileName { get; set; }

        public DateTimeOffset UploadDate { get; private set; }

        public DateTimeOffset LastSyncDate { get; set; }
    }
}
