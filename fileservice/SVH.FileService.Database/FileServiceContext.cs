using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using SVH.FileService.Database.Models;
using DbContext = Microsoft.EntityFrameworkCore.DbContext;

namespace SVH.FileService.Database
{
    public class FileServiceContext : DbContext
    {
        private readonly string _connectionString;

        public virtual DbSet<FileDbModel> Files { get; set; }

        public virtual DbSet<ConversionDbModel> Conversions { get; set; }

        public FileServiceContext(DbContextOptions dbContextOptions, IOptions<DatabaseSettings> opts)
            : base(dbContextOptions)
        {
            _connectionString = opts.Value.ConnectionString;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {

        }

        public void InitData()
        {

        }
    }
}
