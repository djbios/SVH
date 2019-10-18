using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using SVH.FileService.Core.Enums;
using SVH.FileService.Core.Rabbit;
using SVH.FileService.Core.Rabbit.Messages;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using SVH.FileService.Database.Models;
using Xabe.FFmpeg;
using Xabe.FFmpeg.Streams;

namespace SVH.FileService.Core.Services
{
    public class ConversionService : IConversionService
    {
        private readonly FileServiceContext _context;
        private readonly IStorage _storage;
        private readonly RabbitPublisher _rabbitPublisher;

        public ConversionService(FileServiceContext context, IStorage storage, RabbitPublisher rabbitPublisher)
        {
            _context = context;
            _storage = storage;
            _rabbitPublisher = rabbitPublisher;
        }

        public async Task ConvertInFormat(Guid videoFileId, VideoFormat format)
        {
            Guid newFileId;
            if (format == VideoFormat.preview)
                newFileId = await GenerateFilePreview(videoFileId);
            else if (format == VideoFormat.gif)
                newFileId = await GenerateFileGif(videoFileId);
            else
            {
                var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == videoFileId)
                           ?? throw new FileNotFoundException();
                var path = await _storage.GetFilePath(file.FileName);
                var newFilePath =
                    await _storage.GeneratePath($"{videoFileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}_{format}.mp4");
                IMediaInfo mediaInfo = await MediaInfo.Get(path);
                IStream videoStream = mediaInfo.VideoStreams.FirstOrDefault().SetFormat(format);

                await Conversion.New().AddStream(videoStream)
                    .SetOutput(newFilePath)
                    .Start();
                var newFile = _context.Files.Add(new FileDbModel(newFilePath));
                await _context.SaveChangesAsync();
                newFileId = newFile.Entity.FileId;
            }

            _rabbitPublisher.Publish<VideoConvertedEventMessage>(new VideoConvertedEventMessage
            {
                Format = format,
                SourceId = videoFileId,
                ResultId = newFileId
            });
        }

        private async Task<Guid> GenerateFilePreview(Guid videoFileId)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == videoFileId)
                       ?? throw new FileNotFoundException();
            var path = await _storage.GetFilePath(file.FileName);
            var previewPath = await _storage.GeneratePath($"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}.jpg");

            Random rnd = new Random();
            for (int i = 0; i < 20; i++)
            {
                await Conversion.Snapshot(path, previewPath, TimeSpan.FromSeconds(rnd.Next(2, 20))).Start();
                    
                var avgColor = await GetAverageColor(previewPath);
                if (avgColor.Item1 + avgColor.Item2 + avgColor.Item3 > 20) //todo
                    break;
            }

            var result = _context.Files.Add(new FileDbModel(previewPath)).Entity;
            await _context.SaveChangesAsync();
            return result.FileId;
        }

        private async Task<Guid> GenerateFileGif(Guid videoFileId)
        {
            var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == videoFileId)
                       ?? throw new FileNotFoundException();
            var path = await _storage.GetFilePath(file.FileName);
            var previewPath = await _storage.GeneratePath($"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}.gif");

            await Conversion.ToGif(path, previewPath, 0).Start();

            var result = _context.Files.Add(new FileDbModel(previewPath)).Entity;
            await _context.SaveChangesAsync();
            return result.FileId;
        }

        private Task<(int, int, int)> GetAverageColor(string path)
        {
            return Task.FromResult((255, 255, 255)); //todo
        }
    }
}
