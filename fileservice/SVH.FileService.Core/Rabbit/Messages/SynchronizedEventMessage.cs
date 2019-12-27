namespace SVH.FileService.Core.Rabbit.Messages
{
    public class SynchronizedEventMessage : MessageBase
    {
        public int Added { get; set; }

        public int Deleted { get; set; }

        public int TotalNow { get; set; }

        public override string TargetEndpoint => "Events";
    }
}
