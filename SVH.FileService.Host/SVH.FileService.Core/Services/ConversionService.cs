﻿using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using SVH.FileService.Core.Rabbit;
using SVH.FileService.Core.Rabbit.Messages;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using SVH.FileService.Database.Models;
using Xabe.FFmpeg;
using Xabe.FFmpeg.Streams;
using Microsoft.Extensions.Options;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Advanced;
using SixLabors.ImageSharp.PixelFormats;
using SVH.FileService.Common.Enums;
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
            FileDbModel result;

            var conversion =
                await _context.Conversions.FirstOrDefaultAsync(c =>
                    c.Source.FileId == videoFileId && c.VideoFormat == format);
            
            if (conversion?.Status == ConversionStatus.InProgress)
                return;

            if (conversion?.Status == ConversionStatus.Success)
                result = conversion.Result;

            else
            {
                var file = await _context.Files.FirstOrDefaultAsync(f => f.FileId == videoFileId)
                           ?? throw new FileNotFoundException();

                if (conversion == null)
                {
                    conversion = new ConversionDbModel
                    {
                        Source = file,
                        Status = ConversionStatus.InProgress,
                        Tryes = 1,
                        VideoFormat = format
                    };
                    _context.Add(conversion);
                }
                else
                    conversion.Tryes++; //todo maxTryes

                await _context.SaveChangesAsync();

                if (format == VideoFormat.preview)
                    result = await GenerateFilePreview(file);

                else if (format == VideoFormat.gif)
                    result = await GenerateFileGif(file);

                else
                    result = await ConvertVideoInternal(file, format);

                _context.Files.Add(result);
                _context.SaveChanges();
            }

            _rabbitPublisher.Publish<VideoConvertedEventMessage>(new VideoConvertedEventMessage
            {
                Format = format,
                SourceId = videoFileId,
                ResultId = result.FileId
            });
        }

        private async Task<FileDbModel> ConvertVideoInternal(FileDbModel file, VideoFormat format)
        {
            var path = await _storage.GetFullFilePath(file.FileName);
            var newFilePath =
                await _storage.GeneratePath(
                    $"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}_{format}.mp4");
            IMediaInfo mediaInfo = await MediaInfo.Get(path);
            IStream videoStream = mediaInfo.VideoStreams.FirstOrDefault().SetFormat(format);

            await Conversion.New().AddStream(videoStream)
                .SetOutput(newFilePath)
                .Start();

            return new FileDbModel(newFilePath);
        }

        private async Task<FileDbModel> GenerateFilePreview(FileDbModel file)
        {
            var path = await _storage.GetFullFilePath(file.FileName);
            var previewPath = await _storage.GeneratePath($"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}.jpg");

            IMediaInfo mediaInfo = await MediaInfo.Get(path);
            var videoStream = mediaInfo.VideoStreams.FirstOrDefault() ?? throw new Exception($"Empty video stream {path}");
            Random rnd = new Random();
            for (int i = 0; i < 20; i++)
            {
                _storage.RemoveFile(previewPath);
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

                    if (GetAverageColor(previewPath) > 30) 
                        break;

                    _storage.RemoveFile(previewPath);
                }
                catch (ConversionException e)
                {
                    Console.WriteLine(e);
                }
            }

            return new FileDbModel(previewPath);
        }

        private async Task<FileDbModel> GenerateFileGif(FileDbModel file)
        {
            var path = await _storage.GetFullFilePath(file.FileName);
            var previewPath = await _storage.GeneratePath($"{file.FileId}_{DateTimeOffset.Now.ToUnixTimeSeconds()}.gif");

            await Conversion.ToGif(path, previewPath, 0).Start();

            return new FileDbModel(previewPath);
        }

        private int GetAverageColor(string path)
        {
            using (var image = Image.Load(path) as Image<Rgba32>)
            {
                double a = 0d;
                for (int x = 0; x < image.Height; x++)
                    a += image.GetPixelRowSpan(x).ToArray().Average(p => (p.R + p.G + p.B) / 3);
                a = a / image.Height;
                return (int) Math.Round(a);
            }
        }
    }
}
