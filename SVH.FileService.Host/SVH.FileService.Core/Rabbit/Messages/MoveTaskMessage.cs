namespace SVH.FileService.Core.Rabbit.Messages
{
    public class MoveTaskMessage : MessageBase
    {
    public string Source { get; set; }

    public string Target { get; set; }
    public override string TargetEndpoint => "Tasks";
    }
}
