namespace SVH.FileService.Core.Rabbit.Messages
{
    public class SynchronizedMessage
    {
        public int Added { get; set; }

        public int Deleted { get; set; }

        public int TotalNow { get; set; }
    }
}
