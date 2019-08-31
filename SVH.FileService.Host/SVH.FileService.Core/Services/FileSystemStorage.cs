using System.Collections.Generic;
using System.IO;
using System.IO.Abstractions;
using System.Linq;
using System.Threading.Tasks;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Core.Services
{
    public class FileSystemStorage : IFileSystemStorage
    {
        private readonly IFileSystem _fileSystem;

        public FileSystemStorage(IFileSystem fileSystem)
        {
            _fileSystem = fileSystem;
        }

        public async Task<ICollection<string>> ScanDirectory(string path)
        {
            List<string> result = _fileSystem.Directory.EnumerateFiles(path).ToList();
            foreach (var directory in _fileSystem.Directory.EnumerateDirectories(path))
            {
                result.AddRange(await ScanDirectory(directory));
            }
            return result;
        }

        public async Task<Stream> GetFileContent(string path)
        {
            return await Task.FromResult(File.OpenRead(path));
        }
    }
}
