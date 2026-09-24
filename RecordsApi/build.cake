// build.cake -- Cake (C# Make) build script for RecordsApi.
// Requires the local Cake.Tool declared in .config/dotnet-tools.json
// (bootstrap with `dotnet tool restore`, which needs nuget.org access).

var target = Argument("target", "Build");
var configuration = Argument("configuration", "Release");

Task("Clean")
    .Does(() =>
{
    CleanDirectories($"./bin/{configuration}");
    CleanDirectories($"./obj");
});

Task("Restore")
    .IsDependentOn("Clean")
    .Does(() =>
{
    DotNetRestore("./RecordsApi.csproj");
});

Task("Build")
    .IsDependentOn("Restore")
    .Does(() =>
{
    DotNetBuild("./RecordsApi.csproj", new DotNetBuildSettings
    {
        Configuration = configuration,
        NoRestore = true,
    });
});

RunTarget(target);
