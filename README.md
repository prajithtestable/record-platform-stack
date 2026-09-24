# record-platform-stack — P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MICRO

This branch is one cell of the **Project 1 / 9 Block** matrix — SCM x build
tool x package manager x architecture. All 96 branches in this matrix ship
the same ReactJS + ASP.NET Core + SQL Server application; they differ only
in the axes below.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| SCM                | Bitbucket |
| Build tool         | SDK-style MSBuild |
| Package manager    | Paket |
| Architecture note  | Microservices |

> **Build tool note:** Invoked directly via `dotnet msbuild` against the SDK-style .csproj (the same MSBuild engine `dotnet build` wraps, called explicitly).

> **Package manager note:** Package resolution is delegated to Paket via a root `paket.dependencies` and `RecordsApi/paket.references`, imported through `.paket/Paket.Restore.targets`. Bootstrapping Paket itself (`paket install`) requires nuget.org access and was **not** verified in this template's sandbox.

> **Architecture-note caveat:** like the rest of this corpus, "Microservices" is a
> label only. Every branch ships the same single `RecordsApi` service described
> below — the architecture note does not change the code, only how this branch's
> use case is framed.

> **Development style:** "Entire Architecture (Model, View, Controller)" — Model
> and Controller are the EF Core entities and ASP.NET Core controllers in
> `RecordsApi`; View is realized as the separately-served React SPA in
> `ClientApp` rather than Razor views, since this is an API + SPA pairing
> rather than a server-rendered MVC app. Documented here rather than silently
> assumed.

> **Verification note:** `ClientApp` was verified in the sandbox this template
> was authored in (`npm install` and `npm run build` both completed
> successfully). `RecordsApi` (and anything requiring `nuget.org`, such as
> Paket or Cake.Tool bootstrapping) could **not** be restore/build-verified
> there — nuget.org was not reachable from that sandbox. The C# code, project
> files, and build/package-manager configuration here were written correctly
> from knowledge but are unverified; they should build normally with open
> network access to nuget.org.

## Locked technology baseline

- **Frontend**: ReactJS (Vite-based dev/build tooling)
- **Backend**: ASP.NET Core 8 Web API
- **Database**: SQL Server 2022 (via EF Core, `Microsoft.EntityFrameworkCore.SqlServer`)
- **CI**: Bitbucket (`bitbucket-pipelines.yml`), building the API with this
  branch's own build tool (SDK-style MSBuild) before building the client.

## Repository shape

```
/ClientApp               React (Vite) app — Records list/add/delete UI, calls RecordsApi over HTTP
/RecordsApi               ASP.NET Core 8 Web API — Records CRUD controller, EF Core DbContext, SQL Server
docker-compose.yml        SQL Server 2022 + RecordsApi + ClientApp (nginx-served build)
```

**Flow**: the React SPA calls `RecordsApi`'s `/api/records` endpoints (GET/POST/PUT/DELETE)
→ `RecordsController` uses `AppDbContext` (EF Core) to read/write the `Records` table in
SQL Server, creating the schema on startup via `EnsureCreated()`.

## Running this branch

Fastest path — everything in containers:

```bash
docker compose up --build
```

Or run each piece locally:

```bash
# API (SQL Server must be reachable at the connection string in appsettings.json)
dotnet msbuild RecordsApi/RecordsApi.csproj -restore -p:Configuration=Release
cd RecordsApi && dotnet run

# client
cd ClientApp
npm ci
npm run dev
```
