using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Mappings;
using SVH.FileService.Core.Models;
using SVH.FileService.Core.Rabbit;
using SVH.FileService.Core.Rabbit.Messages;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using SVH.FileService.Database.Models;
using Z.EntityFramework.Plus;

namespace SVH.FileService.Core.Services
{
    public class FileService : IFileService
    {
        private readonly FileServiceContext _context;
        private readonly IStorage _storage;
        private readonly FileServiceSettings _settings;
        private readonly RabbitPublisher _rabbitPublisher;
        
        public FileService(FileServiceContext context, IStorage storage, IOptions<FileServiceSettings> opts, RabbitPublisher rabbitPublisher)
        {
            _context = context;
            _storage = storage;
            _rabbitPublisher = rabbitPublisher;
            _settings = opts.Value;
        }

        public async Task<ICollection<FileDto>> GetFiles(bool rescan)
        {
            if (rescan)
            {
                var results = await Rescan();
                _rabbitPublisher.Publish<SynchronizedMessage>(new SynchronizedMessage
                {
                    TotalNow = results.total,
                    Added = results.added,
                    Deleted = results.deleted
                });
            }

            return _context.Files.ToList().ToDtoCollection(await _storage.GeneratePath(""));
        }

        public async Task<string> GetFileName(Guid id)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == id);
            return file.FileName;
        }

        private async Task<(int added, int deleted, int total)> Rescan()
        {
            var now = DateTimeOffset.UtcNow;
            int added = 0;
            int deleted = 0;
            int total = 0;
            var paths = await _storage.ScanBucket("sources");
            foreach (var path in paths)
            {
                var existent = await _context.Files.Where(f => f.FileName == path).FirstOrDefaultAsync();
                if (existent == null)
                {
                    var file = new FileDbModel(path);
                    file.LastSyncDate = now;
                    await _context.Files.AddAsync(file);
                    added++;
                }
                else
                {
                    existent.LastSyncDate = now;
                }
                total++;
            }
            
            await _context.SaveChangesAsync();
            var old = _context.Files.Where(f => f.LastSyncDate < now);
            deleted = old.Delete();
            return (added, deleted, total);
        }
    }
}
