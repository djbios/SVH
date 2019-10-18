using System.Collections.Generic;

namespace SVH.FileService.Core.Configuration
{
    public class RabbitSettings
    {
        public string Host { get; set; }

        public string Password { get; set; }

        public string UserName { get; set; }

        public int Port { get; set; }

        public Dictionary<string, RabbitEndpoint> RabbitEndpoints { get; set; }

        public string VirtualHost { get; set; }
    }
}
