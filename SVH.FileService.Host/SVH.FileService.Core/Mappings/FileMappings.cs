using System.Collections.Generic;
using System.Runtime.InteropServices.ComTypes;
using AutoMapper;
using SVH.FileService.Core.Models;
using SVH.FileService.Database.Models;

namespace SVH.FileService.Core.Mappings
{
    internal static class FileMappings
    {
        private static readonly IMapper Mapper;
        static FileMappings()
        {
            var config = new MapperConfiguration(cfg =>
            {
                cfg.CreateMap<FileDbModel, FileDto>();
            });

            Mapper = config.CreateMapper();
        }

        public static ICollection<FileDto> ToDtoCollection(this ICollection<FileDbModel> dbModels)
        {
            return Mapper.Map<ICollection<FileDto>>(dbModels);
        }
    }
}
