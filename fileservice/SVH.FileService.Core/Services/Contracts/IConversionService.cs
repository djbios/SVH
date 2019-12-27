using System;
using System.Threading.Tasks;
using SVH.FileService.Common.Enums;

namespace SVH.FileService.Core.Services.Contracts
{
    public interface IConversionService
    {
        Task ConvertInFormat(Guid videoFileId, VideoFormat format);
    }
}
