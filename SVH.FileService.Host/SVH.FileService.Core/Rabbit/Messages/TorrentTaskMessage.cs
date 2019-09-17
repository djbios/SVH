namespace SVH.FileService.Core.Rabbit.Messages
{
    public class TorrentTaskMessage
    {
        public string MagnetUrl { get; set; }

        public string Location { get; set; }
    }
}
