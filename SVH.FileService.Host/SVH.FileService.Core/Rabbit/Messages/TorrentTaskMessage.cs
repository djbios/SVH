namespace SVH.FileService.Core.Rabbit.Messages
{
    public class TorrentTaskMessage : MessageBase
    {
        public string MagnetUrl { get; set; }

        public string Location { get; set; }

        public override string TargetEndpoint => "Tasks";
    }
}
