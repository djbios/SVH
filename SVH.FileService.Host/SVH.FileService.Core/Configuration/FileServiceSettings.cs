namespace SVH.FileService.Core.Configuration
{
    public struct PictureSize
    {
        public int Height { get; set; }

        public int Width { get; set; }
    }

    public class FileServiceSettings
    {
        public string MediaPath { get; set; }

        public PictureSize DefaultPreviewSize { get; set; }
    }
}