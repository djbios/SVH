using System;
using System.Threading.Tasks;
using SVH.FileService.Core.Models;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IPreviewService
    {
        Task<FileDto> GenerateFilePreview(Guid videoFileId);
    }
}
