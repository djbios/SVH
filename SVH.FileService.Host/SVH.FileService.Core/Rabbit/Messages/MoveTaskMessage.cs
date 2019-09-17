namespace SVH.FileService.Core.Rabbit.Messages
{
    public class MoveTaskMessage
    {
        public string Source { get; set; }

        public string Target { get; set; }
    }
}
