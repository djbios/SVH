﻿using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using SVH.FileService.Database.Models;

namespace SVH.FileService.Database
{
    public class FileServiceContext : DbContext
    {
        private readonly string _connectionString;

        public DbSet<FileDbModel> Files { get; set; }

        public FileServiceContext(DbContextOptions dbContextOptions, IOptions<DatabaseSettings> opts)
            : base(dbContextOptions)
        {
            _connectionString = opts.Value.ConnectionString;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql(_connectionString);
        }

        public void InitData()
        {

        }
    }
}
