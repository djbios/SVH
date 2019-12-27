using System.Collections.Generic;
using System.IO;
using System.IO.Abstractions;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Options;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Exceptions;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Core.Services
{
    public class FileSystemStorage : IStorage
    {
        private readonly IFileSystem _fileSystem;
        private readonly string _root;

        public FileSystemStorage(IFileSystem fileSystem, IOptions<FileServiceSettings> opts)
        {
            _fileSystem = fileSystem;
            _root = opts.Value.MediaPath;
        }

        public async Task<ICollection<string>> ScanBucket(string relativePath)
        {
            var path = Path.Combine(_root, relativePath);
            Directory.CreateDirectory(path); // if not exists
            List<string> result = _fileSystem.Directory.EnumerateFiles(path).ToList();
            foreach (var directory in _fileSystem.Directory.EnumerateDirectories(path))
            {
                var subs = await ScanBucket(directory);
                result.AddRange(subs);
            }

            return result.UnixifyPaths(_root);
        }

        public Task<string> GeneratePath(string filename)
        {
            return Task.FromResult(Path.Combine(_root, filename));
        }

        public Task Move(string source, string destination)
        {
            source = source.TrimStart('\\').TrimStart('/');
            destination = destination.TrimStart('\\').TrimStart('/');

            var sPath = Path.Combine(_root, source);
            var dPath = Path.Combine(_root, destination);

            if (_fileSystem.Directory.Exists(sPath))
                _fileSystem.Directory.Move(sPath, dPath);
            else if (_fileSystem.File.Exists(sPath))
                _fileSystem.File.Move(sPath, dPath);
            else
                throw new IncorrectPathException("source");

            return Task.CompletedTask;
        }

        public Task<string> GetFullFilePath(string fileName)
        {
            return Task.FromResult(Path.Combine(_root, fileName));
        }

        public void RemoveFile(string path)
        {
            if(File.Exists(path))
                _fileSystem.File.Delete(path);
        }
    }
}
