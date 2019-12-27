using System.IO;
using System.IO.Abstractions;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;
using SVH.FileService.Core.Configuration;
using SVH.FileService.Core.Rabbit;
using SVH.FileService.Core.Services;
using SVH.FileService.Core.Services.Contracts;
using SVH.FileService.Database;
using Xabe.FFmpeg;

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

            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_3_0);

            services.Configure<FileServiceSettings>(Configuration.GetSection(nameof(FileServiceSettings)));
            services.Configure<DatabaseSettings>(Configuration.GetSection(nameof(DatabaseSettings)));
            services.Configure<RabbitSettings>(Configuration.GetSection(nameof(RabbitSettings)));


            services.AddSingleton<IFileSystem, FileSystem>();
            services.AddSingleton<IStorage, FileSystemStorage>();
            services.AddTransient<IFileService, Core.Services.FileService>();
            services.AddTransient<IConversionService, ConversionService>();

            services.AddDbContext<FileServiceContext>(options =>
                options.UseNpgsql(Configuration.GetConnectionString("Postgres")));


            services.AddHostedService<RabbitConsumer>();
            services.AddSingleton<RabbitPublisher>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
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

            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                // Mapping of endpoints goes here:
                endpoints.MapControllers();
            });
            
            FFmpeg.GetLatestVersion();
            if (Path.IsPathFullyQualified("C:\\Windows"))
                FFmpeg.ExecutablesPath = "C:\\Windows";
        }
    }
}
