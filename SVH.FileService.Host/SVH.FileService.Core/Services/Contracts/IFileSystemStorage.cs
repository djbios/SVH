using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IFileSystemStorage
    {
        Task<ICollection<string>> ScanDirectory(string path = "D:\\media");

        Task<Stream> GetFileContent(string path);
    }
}
