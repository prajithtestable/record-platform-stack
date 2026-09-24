# Multi-stage build for RecordsApi (ASP.NET Core 8 Web API)
#
# NOTE: building this image requires NuGet package restore (nuget.org).
# In the sandbox this template was authored in, nuget.org was not reachable,
# so this Dockerfile is written correctly from knowledge but has NOT been
# build-verified there. It should build normally in an environment with
# open network access to nuget.org.

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY RecordsApi.csproj ./
RUN dotnet restore RecordsApi.csproj

COPY . .
RUN dotnet publish RecordsApi.csproj -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "RecordsApi.dll"]
