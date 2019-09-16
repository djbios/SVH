using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using RabbitMQ.Client;
using RabbitMQ.Client.Framing;
using SVH.FileService.Core.Configuration;

namespace SVH.FileService.Core.Rabbit
{
    public class RabbitPublisher : IDisposable
    {
        private readonly ILogger _logger;

        private readonly IModel _channel;

        private readonly IConnection _connection;

        private readonly IServiceProvider _serviceProvider;

        private readonly RabbitSettings _settings;

        public RabbitPublisher(IOptions<RabbitSettings> options, IServiceProvider serviceProvider, ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger<RabbitConsumer>();

            _serviceProvider = serviceProvider;
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
          
            _channel.ExchangeDeclare(_settings.Exchange, ExchangeType.Topic);
            _channel.QueueDeclare(_settings.Queue, false, false, false, null);
            }

        public void Publish<T>(object message)
        {
            if (message == null)
            {
                throw new ArgumentNullException($"Required value for {nameof(message)}");
            }

            var jsonMessage = JsonConvert.SerializeObject(message);
            var bytesMessage = Encoding.UTF8.GetBytes(jsonMessage);

            var props = new BasicProperties
            {
                Headers = new Dictionary<string, object>
                {
                    { AppConstants.RabbitMessageTypeHeaderName, typeof(T).Name }
                }
            };
            
            _channel.BasicPublish(_settings.Exchange, _settings.RoutingKey, props, bytesMessage);
            _logger.LogInformation($"Message sent {jsonMessage}");
        }

        public void Dispose()
        {
            _channel.Close();
            _connection.Close();
        }
    }
}
