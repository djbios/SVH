namespace SVH.FileService.Core.Rabbit.Messages
{
    public abstract class MessageBase
    {
        public abstract string TargetEndpoint { get; }
    }
}
