using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IStorage
    {
        Task<ICollection<string>> ScanBucket(string path);

        Task<string> GetPath(string fileName, string bucketName = "");
    }
}
