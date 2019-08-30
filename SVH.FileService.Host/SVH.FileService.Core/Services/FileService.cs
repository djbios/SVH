using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
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
        private readonly IFileSystemStorage _storage;

        public FileService(FileServiceContext context, IFileSystemStorage storage)
        {
            _context = context;
            _storage = storage;
        }

        public async Task<ICollection<FileDto>> GetFiles(bool rescan)
        {
            if (rescan)
                await Rescan();
            return _context.Files.ToList().ToDtoCollection();
        }

        public async Task<string> GetFileName(Guid id)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == id);
            return file.FileName;
        }

        private async Task Rescan()
        {
            var paths = await _storage.ScanDirectory();
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
