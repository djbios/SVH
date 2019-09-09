using SVH.FileService.Database;

namespace SVH.FileService.Core.Services
{
    public class PreviewService
    {
        FileServiceContext _context;

        public PreviewService(FileServiceContext context)
        {
            _context = context;
        }
    }
}
