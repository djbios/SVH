using Microsoft.EntityFrameworkCore;
using SVH.FileService.Database.Models;

namespace SVH.FileService.Database
{
    public class FileServiceContext : DbContext
    {
        public DbSet<FileDbModel> Files { get; set; }

        public FileServiceContext(DbContextOptions dbContextOptions)
            : base(dbContextOptions)
        {
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=svhFiles;Username=svh;");
        }

        public void InitData()
        {

        }
    }
}
