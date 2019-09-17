using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Abstractions;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.OpenApi.Models;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Rabbit;
using SVH.FileService.Core.Services;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;

namespace SVH.FileService.Host
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddSwaggerGen(c =>
                c.SwaggerDoc("v1", new OpenApiInfo()
                {
                    Title = "SVH Files service",
                    Version = "v1"
                }));

            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);

            services.AddSingleton<IFileSystem, FileSystem>();
            services.AddSingleton<IStorage, FileSystemStorage>();
            services.AddTransient<IFileService, Core.Services.FileService>();
            services.AddTransient<IConversionService, ConversionService>();
            services.Configure<DatabaseSettings>(Configuration.GetSection(nameof(DatabaseSettings)));
            services.AddEntityFrameworkNpgsql().AddDbContext<FileServiceContext>()
                .BuildServiceProvider();


            services.Configure<FileServiceSettings>(Configuration.GetSection(nameof(FileServiceSettings)));
            services.AddHostedService<RabbitConsumer>();
            services.AddSingleton<RabbitPublisher>();
            services.Configure<RabbitSettings>(Configuration.GetSection(nameof(RabbitSettings)));
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            app.UseSwagger();

            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "Files API V1");
                c.RoutePrefix = string.Empty;
            });

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseMvc();
            
        }
    }
}
