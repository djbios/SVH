using System.Collections.Generic;
using System.Threading.Tasks;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IStorage
    {
        Task<ICollection<string>> ScanBucket(string path);

        Task<string> GeneratePath(string filename);

        Task Move(string source, string destination);

        Task<string> GetFullFilePath(string fileName);

        void RemoveFile(string path);
    }
}
