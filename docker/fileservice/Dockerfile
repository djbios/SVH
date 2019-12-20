FROM microsoft/dotnet:2.2-sdk AS build-env
WORKDIR /app
COPY SVH.FileService.Host /app
RUN dotnet publish ./SVH.FileService.Host -c Release -o /app/out

# Build runtime image
FROM microsoft/dotnet:2.2-aspnetcore-runtime
WORKDIR /app
COPY --from=build-env /app/out .
ENTRYPOINT ["dotnet", "SVH.FileService.Host.dll"]
