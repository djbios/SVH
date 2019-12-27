namespace SVH.FileService.Core.Configuration
{
    public class RabbitEndpoint
    {
        public string Exchange { get; set; }

        public string ExchangeType { get; set; }
        
        public string Queue { get; set; }

        public string RoutingKey { get; set; }
    }
}
