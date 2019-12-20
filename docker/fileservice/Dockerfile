FROM mcr.microsoft.com/dotnet/core/sdk:3.0 AS build-env
WORKDIR /app
COPY SVH.FileService.Host /app
RUN dotnet publish ./SVH.FileService.Host -c Release -o /app/out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.0
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "SVH.FileService.Host.dll"]
