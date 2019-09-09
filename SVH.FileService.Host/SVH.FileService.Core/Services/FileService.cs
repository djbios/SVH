using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Mappings;
using SVH.FileService.Core.Models;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using SVH.FileService.Database.Models;

namespace SVH.FileService.Core.Services
{
    public class FileService : IFileService
    {
        private readonly FileServiceContext _context;
        private readonly IStorage _storage;
        private readonly FileServiceSettings _settings;
        
        public FileService(FileServiceContext context, IStorage storage, IOptions<FileServiceSettings> opts)
        {
            _context = context;
            _storage = storage;
            _settings = opts.Value;
        }

        public async Task<ICollection<FileDto>> GetFiles(bool rescan)
        {
            if (rescan)
                await Rescan();
            return _context.Files.ToList().ToDtoCollection(await _storage.GetPath("", "sources"));
        }

        public async Task<string> GetFileName(Guid id)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == id);
            return file.FileName;
        }

        private async Task Rescan()
        {
            var paths = await _storage.ScanBucket("sources");
            foreach (var path in paths)
            {
                var existent = await _context.Files.Where(f => f.FileName == path).FirstOrDefaultAsync();
                if (existent == null)
                {
                    var file = new FileDbModel
                    {
                        FileId = Guid.NewGuid(),
                        FileName = path
                    };
                    await _context.Files.AddAsync(file);
                }
            }

            await _context.SaveChangesAsync();
        }
    }
}
