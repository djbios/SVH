using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using RabbitMQ.Client;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Rabbit.Messages;

namespace SVH.FileService.Core.Rabbit
{
    public class RabbitPublisher : IDisposable
    {
        private readonly ILogger _logger;

        private readonly IModel _channel;

        private readonly IConnection _connection;

        private readonly RabbitSettings _settings;

        public RabbitPublisher(IOptions<RabbitSettings> options, ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<RabbitPublisher>();

            _settings = options.Value;

            var factory = new ConnectionFactory
            {
                HostName = _settings.Host,
                Password = _settings.Password,
                UserName = _settings.UserName,
                Port = _settings.Port,
                VirtualHost = _settings.VirtualHost
            };

            _connection = factory.CreateConnection();

            _channel = _connection.CreateModel();
            foreach (var ep in _settings.RabbitEndpoints.Values)
            {
                _channel.ExchangeDeclare(ep.Exchange, ep.ExchangeType);
            }

            //_channel.QueueDeclare(_settings.Queue, false, false, false, null);
            }

        public void Publish<T>(MessageBase message)
        {
            if (message == null)
            {
                throw new ArgumentNullException($"Required value for {nameof(message)}");
            }

            var jsonMessage = JsonConvert.SerializeObject(message);
            var bytesMessage = Encoding.UTF8.GetBytes(jsonMessage);
            var model = _connection.CreateModel();
            var props = model.CreateBasicProperties();

            props.Headers = new Dictionary<string, object> {{AppConstants.RabbitMessageTypeHeaderName, typeof(T).Name}};
            var endpoint = _settings.RabbitEndpoints[message.TargetEndpoint];
            _channel.BasicPublish(endpoint.Exchange, endpoint.RoutingKey, props, bytesMessage);
            _logger.LogInformation($"Message sent {jsonMessage}");
        }

        public void Dispose()
        {
            _channel.Close();
            _connection.Close();
        }
    }
}
