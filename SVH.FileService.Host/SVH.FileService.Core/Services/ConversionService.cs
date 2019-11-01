﻿using System;
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
using System.Drawing;
using Microsoft.Extensions.Options;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Advanced;
using SixLabors.ImageSharp.ColorSpaces;
using SixLabors.ImageSharp.ColorSpaces.Conversion;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using SVH.FileService.Core.Configuration;
using Xabe.FFmpeg.Enums;
using Xabe.FFmpeg.Exceptions;

namespace SVH.FileService.Core.Services
{
    public class ConversionService : IConversionService
    {
        private readonly FileServiceContext _context;
        private readonly IStorage _storage;
        private readonly RabbitPublisher _rabbitPublisher;
        private readonly IOptions<FileServiceSettings> _settings;

        public ConversionService(FileServiceContext context, IStorage storage, RabbitPublisher rabbitPublisher, IOptions<FileServiceSettings> settings)
        {
            _context = context;
            _storage = storage;
            _rabbitPublisher = rabbitPublisher;
            _settings = settings;
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

            IMediaInfo mediaInfo = await MediaInfo.Get(path);
            var videoStream = mediaInfo.VideoStreams.FirstOrDefault() ?? throw new Exception($"Empty video stream {path}");
            Random rnd = new Random();
            for (int i = 0; i < 20; i++)
            {
                var targetSec = rnd.Next(1, videoStream.Duration.Seconds);
                try
                {
                    await Conversion.New().AddStream(videoStream
                            .SetCodec(VideoCodec.Png)
                            .SetOutputFramesCount(1)
                            .SetSize(new VideoSize(_settings.Value.DefaultPreviewSize.Width,
                                _settings.Value.DefaultPreviewSize.Height))
                            .SetSeek(TimeSpan.FromSeconds(targetSec)))
                        .SetOutput(previewPath)
                        .Start();
                }
                catch (ConversionException e)
                {
                    Console.WriteLine(e);
                }

                if (GetAverageColor(previewPath) > 30) 
                    break;
                _storage.RemoveFile(previewPath);
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

        private int GetAverageColor(string path)
        {
            using (var image = Image.Load(path) as Image<Rgba32>)
            {
                double a = 0d;
                for (int x = 0; x < image.Height; x++)
                    a += image.GetPixelRowSpan(x).ToArray().Average(p => (p.R + p.G + p.B) / 3);
                a = a / image.Height;
                return (int)Math.Round(a);
            }
        }
    }
}
