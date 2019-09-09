using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using SVH.FileService.Core.Mappings;
using SVH.FileService.Core.Models;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using SVH.FileService.Database.Models;
using Xabe.FFmpeg;

namespace SVH.FileService.Core.Services
{
    public class PreviewService : IPreviewService
    {
        private readonly FileServiceContext _context;
        private readonly IStorage _storage;

        public PreviewService(FileServiceContext context, IStorage storage)
        {
            _context = context;
            _storage = storage;
        }

        public async Task<FileDto> GenerateFilePreview(Guid videoFileId)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == videoFileId)
                       ?? throw new FileNotFoundException();
            var previewPath = await _storage.GetPath($"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}.jpg", "previews");

            Random rnd = new Random();
            for (int i = 0; i < 20; i++)
            {
                await Conversion.Snapshot(file.FileName, previewPath, TimeSpan.FromSeconds(rnd.Next(2, 20))).Start();
                    
                var avgColor = await GetAverageColor(previewPath);
                if (avgColor.Item1 + avgColor.Item2 + avgColor.Item3 > 20)
                    break;
            }

            var result = await _context.AddAsync(new FileDbModel
            {
                FileName = previewPath,
                FileId = Guid.NewGuid()
            });

            return result.Entity.ToDto();
        }

        private Task<(int, int, int)> GetAverageColor(string path)
        {
            return Task.FromResult((255, 255, 255)); //todo
        }
    }
}
