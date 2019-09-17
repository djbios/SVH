using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using SVH.FileService.Core.Models;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IFileService
    {
        Task<ICollection<FileDto>> GetFiles(bool rescan);

        Task<string> GetFileName(Guid id);

        Task Move(string source, string destination);
    }
}
