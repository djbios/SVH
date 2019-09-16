using System;
using System.Linq;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Rabbit.Messages;
using SVH.FileService.Core.Services.Contracts;

namespace SVH.FileService.Core.Rabbit
{
    public class RabbitConsumer : BackgroundService
    {
        private readonly ILogger _logger;
        private readonly IConnection _connection;
        private readonly IModel _channel;
        private readonly RabbitSettings _settings;

        private readonly IServiceProvider _serviceProvider;

        public RabbitConsumer(ILoggerFactory loggerFactory, IServiceProvider serviceProvider, IOptions<RabbitSettings> options)
        {
            _serviceProvider = serviceProvider;
            _settings = options.Value;

            _logger = loggerFactory.CreateLogger<RabbitConsumer>();

            var factory = new ConnectionFactory
            {
                HostName = _settings.Host,
                Password = _settings.Password,
                UserName = _settings.UserName,
                Port = _settings.Port,
                VirtualHost = _settings.VirtualHost
            };

            // create connection  
            _connection = factory.CreateConnection();

            // create channel  
            _channel = _connection.CreateModel();

            _channel.ExchangeDeclare(_settings.Exchange, ExchangeType.Topic);
            _channel.QueueDeclare(_settings.Queue, false, false, false, null);
            _channel.QueueBind(_settings.Queue, _settings.Exchange, _settings.RoutingKey, null);
            _channel.BasicQos(0, 1, false);

            _connection.ConnectionShutdown += RabbitMQ_ConnectionShutdown;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            stoppingToken.ThrowIfCancellationRequested();

            var consumer = new EventingBasicConsumer(_channel);
            consumer.Received += async (ch, ea) =>
            {
                try
                {
                    _channel.BasicAck(ea.DeliveryTag, false);
                    await HandleMessage(ea);
                }
                catch (Exception e)
                {
                    _logger.LogError(e.ToString());
                }
            };

            consumer.Shutdown += OnConsumerShutdown;
            consumer.Registered += OnConsumerRegistered;
            consumer.Unregistered += OnConsumerUnregistered;
            consumer.ConsumerCancelled += OnConsumerConsumerCancelled;

            _channel.BasicConsume(_settings.Queue, false, consumer);
        }

        private object GetMessageObject(BasicDeliverEventArgs ea)
        {
            var content = System.Text.Encoding.UTF8.GetString(ea.Body);
            _logger.LogInformation($"consumer received {content}");

            ea.BasicProperties.Headers.TryGetValue(AppConstants.RabbitMessageTypeHeaderName, out object typeBytes);
            var typeName = System.Text.Encoding.UTF8.GetString((byte[]) typeBytes);

            Type messageType = Type.GetType($"SVH.FileService.Core.Rabbit.Messages.{typeName}, SVH.FileService.Core");

            MethodInfo method = typeof(JsonConvert).GetMethods()
                .First(m => m.IsGenericMethod && m.Name == "DeserializeObject");
            MethodInfo genericMethod = method.MakeGenericMethod(messageType);
            var message = genericMethod.Invoke(null, new object[] { content });
            return message;
        }

        private async Task HandleMessage(BasicDeliverEventArgs ea)
        {
            using (var scope = _serviceProvider.CreateScope())
            {
                var conversionService =
                    scope.ServiceProvider
                        .GetRequiredService<IConversionService>();


                var message = GetMessageObject(ea);
                if (message is VideoConvertTaskMessage vcm)
                {
                    await conversionService.ConvertInFormat(vcm.FileId, vcm.Format);
                }
            }
        }

        private void OnConsumerConsumerCancelled(object sender, ConsumerEventArgs e)
        {
        }

        private void OnConsumerUnregistered(object sender, ConsumerEventArgs e)
        {
        }

        private void OnConsumerRegistered(object sender, ConsumerEventArgs e)
        {
        }

        private void OnConsumerShutdown(object sender, ShutdownEventArgs e)
        {
        }

        private void RabbitMQ_ConnectionShutdown(object sender, ShutdownEventArgs e)
        {
        }

        public override void Dispose()
        {
            _channel.Close();
            _connection.Close();
            base.Dispose();
        }
    }
}
