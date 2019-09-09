using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Abstractions;
using System.Linq;
using System.Threading.Tasks;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Core.Services
{
    public class FileSystemStorage : IStorage
    {
        private readonly IFileSystem _fileSystem;
        private const string Root = @"D:\\media";

        public FileSystemStorage(IFileSystem fileSystem)
        {
            _fileSystem = fileSystem;
        }

        public async Task<ICollection<string>> ScanBucket(string relativePath)
        {
            var path = Path.Combine(Root, relativePath);
            List<string> result = _fileSystem.Directory.EnumerateFiles(path).ToList();
            foreach (var directory in _fileSystem.Directory.EnumerateDirectories(path))
            {
                result.AddRange(await ScanBucket(directory));
            }
            return result;
        }

        public Task<string> GetPath(string fileName, string bucketName = "")
        {
           return Task.FromResult(Path.Combine(Root, bucketName, fileName));
        }
    }
}
