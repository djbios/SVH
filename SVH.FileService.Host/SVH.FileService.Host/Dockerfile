FROM microsoft/dotnet:2.2-aspnetcore-runtime AS base
WORKDIR /app
EXPOSE 80

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY ["SVH.FileService.Host/SVH.FileService.Host.csproj", "SVH.FileService.Host/"]
RUN dotnet restore "SVH.FileService.Host/SVH.FileService.Host.csproj"
COPY . .
WORKDIR "/src/SVH.FileService.Host"
RUN dotnet build "SVH.FileService.Host.csproj" -c Release -o /app

FROM build AS publish
RUN dotnet publish "SVH.FileService.Host.csproj" -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "SVH.FileService.Host.dll"]