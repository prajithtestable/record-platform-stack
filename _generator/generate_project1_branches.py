#!/usr/bin/env python3
"""
Generates the "Project 1 / 9 Block" branch matrix for record-platform-stack:

    P1_{SCM}_REACT_DOTNETCORE_{BUILD}_{PKGMGR}_MVC_{ARCH}

Stack (fixed for every branch): ReactJS frontend (Vite) + ASP.NET Core 8
Web API backend + SQL Server (via EF Core), development style = MVC
(Model = EF Core entities, Controller = ASP.NET Core controllers, View =
the React SPA, served separately rather than Razor views — documented as
an explicit substitution in every branch's README, the same way earlier
repos in this corpus disclosed tooling substitutions).

Axes:
  SCM (4):            GitHub, Bitbucket, GitLab, Azure DevOps
                       -> which CI pipeline config file ships at the repo root,
                          and its build step is wired to that branch's own
                          build-tool command (not just a label).
  Build tool (3):      SDK-style MSBuild, Cake, .NET CLI
                       -> how RecordsApi is invoked to build (and by the CI file).
  Package manager (4): NuGet (PackageReference), Paket,
                       Central Package Management, NuGet (packages.config)
                       -> how RecordsApi.csproj resolves its package versions.
  Architecture (2):    Monolith, Microservices
                       -> label only, like the rest of this corpus's
                          Architecture axis; every branch ships the same
                          single-service RecordsApi, and the README says so.

4 x 3 x 4 x 2 = 96 branches.

Inputs (external, not part of this repo, same convention as the sibling
generate_branches.py / generate_sippoy_branches.py):

  TEMPLATE_DIR   a clean copy of ClientApp/, RecordsApi/, docker-compose.yml,
                 .gitignore (no node_modules/dist/bin/obj). The React client
                 (ClientApp) was verified to install and build in this
                 template (`npm install` && `npm run build` both succeeded).
                 The .NET side (RecordsApi) could NOT be restore/build
                 verified in the sandbox this template was authored in --
                 nuget.org was not reachable from it. Its C# source was
                 written correctly from knowledge but is UNVERIFIED.

NOTE: this script deletes every top-level entry of the repo working tree
(except .git) on each iteration, including anything untracked -- so this
file itself must be committed to `main` (not left untracked) before running
it, or it will delete itself mid-run.

Usage: python3 _generator/generate_project1_branches.py
Run from the repo root, on a clean working tree.
"""
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.environ.get("P1_TEMPLATE_DIR", "/tmp/p1-template")

SKIP_COPY_DIRS = {"node_modules", "dist", "bin", "obj", ".git"}

# ---------------------------------------------------------------------------
# Axis definitions
# ---------------------------------------------------------------------------

BUILD_TOOLS = {
    "MSBUILD": {
        "label": "SDK-style MSBuild",
        "build_cmd": "dotnet msbuild RecordsApi/RecordsApi.csproj -restore -p:Configuration=Release",
        "note": "Invoked directly via `dotnet msbuild` against the SDK-style .csproj "
        "(the same MSBuild engine `dotnet build` wraps, called explicitly).",
    },
    "CAKE": {
        "label": "Cake",
        "build_cmd": "dotnet cake RecordsApi/build.cake --target=Build",
        "note": "Driven by `RecordsApi/build.cake`, a Cake (C# Make) script, via the "
        "local `Cake.Tool` .NET tool declared in `.config/dotnet-tools.json`. "
        "Bootstrapping the tool (`dotnet tool restore`) requires nuget.org "
        "access and was **not** verified in this template's sandbox.",
    },
    "CLI": {
        "label": ".NET CLI",
        "build_cmd": "dotnet build RecordsApi/RecordsApi.csproj -c Release",
        "note": "Built with the plain `dotnet build`/`dotnet run` CLI workflow, "
        "with the SDK version pinned via `global.json`.",
    },
}

PACKAGE_MANAGERS = {
    "NUGETPKGREF": {
        "label": "NuGet (PackageReference)",
        "note": "The default SDK-style mechanism: `<PackageReference>` items with "
        "explicit `Version` attributes directly in `RecordsApi.csproj`.",
    },
    "CPM": {
        "label": "Central Package Management",
        "note": "Package versions are centralized in a root `Directory.Packages.props` "
        "(`ManagePackageVersionsCentrally=true`); `RecordsApi.csproj` lists "
        "`<PackageReference>` items with no `Version` attribute.",
    },
    "PAKET": {
        "label": "Paket",
        "note": "Package resolution is delegated to Paket via a root `paket.dependencies` "
        "and `RecordsApi/paket.references`, imported through `.paket/Paket.Restore.targets`. "
        "Bootstrapping Paket itself (`paket install`) requires nuget.org access and was "
        "**not** verified in this template's sandbox.",
    },
    "NUGETCONFIG": {
        "label": "NuGet (packages.config)",
        "note": "**Substitution note:** `packages.config` is not supported by SDK-style "
        "projects (`net8.0`, `Microsoft.NET.Sdk.Web`) — it's a legacy mechanism for "
        "non-SDK, `.NET Framework`-style `.csproj` files only. This branch honestly "
        "keeps `PackageReference` in `RecordsApi.csproj` (identical to the NuGet "
        "(PackageReference) branch) and documents the substitution here rather than "
        "shipping a `packages.config` that .NET 8 would simply ignore.",
    },
}

SCMS = {
    "GITHUB": {"label": "GitHub", "ci_files": lambda cmd: {".github/workflows/ci.yml": _github_ci(cmd)}},
    "BITBUCKET": {"label": "Bitbucket", "ci_files": lambda cmd: {"bitbucket-pipelines.yml": _bitbucket_ci(cmd)}},
    "GITLAB": {"label": "GitLab", "ci_files": lambda cmd: {".gitlab-ci.yml": _gitlab_ci(cmd)}},
    "AZURE": {"label": "Azure DevOps", "ci_files": lambda cmd: {"azure-pipelines.yml": _azure_ci(cmd)}},
}

ARCHITECTURES = {
    "MONO": "Monolith",
    "MICRO": "Microservices",
}


# ---------------------------------------------------------------------------
# CI file templates (per SCM), parametrized by that branch's own build command
# ---------------------------------------------------------------------------

def _github_ci(build_cmd):
    return f"""name: CI

on:
  push:
    branches: [ "**" ]
  pull_request:
    branches: [ "**" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "8.0.x"

      - name: Restore & build API
        run: {build_cmd}

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: Build client
        working-directory: ClientApp
        run: |
          npm ci
          npm run build
"""


def _bitbucket_ci(build_cmd):
    return f"""image: mcr.microsoft.com/dotnet/sdk:8.0

pipelines:
  default:
    - step:
        name: Build API
        script:
          - {build_cmd}
    - step:
        name: Build client
        image: node:22
        script:
          - cd ClientApp
          - npm ci
          - npm run build
"""


def _gitlab_ci(build_cmd):
    return f"""stages:
  - build

build-api:
  stage: build
  image: mcr.microsoft.com/dotnet/sdk:8.0
  script:
    - {build_cmd}

build-client:
  stage: build
  image: node:22
  script:
    - cd ClientApp
    - npm ci
    - npm run build
"""


def _azure_ci(build_cmd):
    return f"""trigger:
  branches:
    include:
      - '*'

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UseDotNet@2
    inputs:
      version: '8.0.x'

  - script: {build_cmd}
    displayName: 'Build API'

  - task: NodeTool@0
    inputs:
      versionSpec: '22.x'

  - script: |
      cd ClientApp
      npm ci
      npm run build
    displayName: 'Build client'
"""


# ---------------------------------------------------------------------------
# Build-tool variant files
# ---------------------------------------------------------------------------

CAKE_BUILD_SCRIPT = """// build.cake -- Cake (C# Make) build script for RecordsApi.
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
"""

CAKE_TOOL_MANIFEST = """{
  "version": 1,
  "isRoot": true,
  "tools": {
    "cake.tool": {
      "version": "4.0.0",
      "commands": [
        "dotnet-cake"
      ]
    }
  }
}
"""

GLOBAL_JSON = """{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestFeature"
  }
}
"""

# ---------------------------------------------------------------------------
# Package-manager variant .csproj / support files
# ---------------------------------------------------------------------------

CSPROJ_PACKAGEREF = """<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.2" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.10" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.10">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

</Project>
"""

CSPROJ_CPM = """<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

</Project>
"""

DIRECTORY_PACKAGES_PROPS = """<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Swashbuckle.AspNetCore" Version="6.6.2" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.10" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.10" />
  </ItemGroup>
</Project>
"""

CSPROJ_PAKET = """<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <!-- Package references are supplied by Paket via paket.references + the root
       paket.dependencies, not by <PackageReference> items here.
       See /paket.dependencies and RecordsApi/paket.references. -->
  <Import Project="../.paket/Paket.Restore.targets" Condition="Exists('../.paket/Paket.Restore.targets')" />

</Project>
"""

PAKET_DEPENDENCIES = """source https://api.nuget.org/v3/index.json

nuget Swashbuckle.AspNetCore 6.6.2
nuget Microsoft.EntityFrameworkCore.SqlServer 8.0.10
nuget Microsoft.EntityFrameworkCore.Design 8.0.10
"""

PAKET_REFERENCES = """Swashbuckle.AspNetCore
Microsoft.EntityFrameworkCore.SqlServer
Microsoft.EntityFrameworkCore.Design
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd, cwd=REPO_ROOT, check=True):
    result = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"FAILED: {cmd}\n{result.stdout}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def copy_template(template_dir, dest_dir):
    for entry in os.listdir(template_dir):
        if entry in SKIP_COPY_DIRS:
            continue
        src = os.path.join(template_dir, entry)
        dst = os.path.join(dest_dir, entry)
        if os.path.isdir(src):
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP_COPY_DIRS))
        else:
            shutil.copy2(src, dst)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def apply_build_tool(repo_root, build_key):
    api_dir = os.path.join(repo_root, "RecordsApi")
    if build_key == "CAKE":
        write(os.path.join(api_dir, "build.cake"), CAKE_BUILD_SCRIPT)
        write(os.path.join(api_dir, ".config", "dotnet-tools.json"), CAKE_TOOL_MANIFEST)
    elif build_key == "CLI":
        write(os.path.join(repo_root, "global.json"), GLOBAL_JSON)
    # MSBUILD: no extra files -- it builds the .csproj that's already there.


def apply_package_manager(repo_root, pm_key):
    api_dir = os.path.join(repo_root, "RecordsApi")
    csproj_path = os.path.join(api_dir, "RecordsApi.csproj")

    if pm_key in ("NUGETPKGREF", "NUGETCONFIG"):
        write(csproj_path, CSPROJ_PACKAGEREF)
    elif pm_key == "CPM":
        write(csproj_path, CSPROJ_CPM)
        write(os.path.join(repo_root, "Directory.Packages.props"), DIRECTORY_PACKAGES_PROPS)
    elif pm_key == "PAKET":
        write(csproj_path, CSPROJ_PAKET)
        write(os.path.join(repo_root, "paket.dependencies"), PAKET_DEPENDENCIES)
        write(os.path.join(api_dir, "paket.references"), PAKET_REFERENCES)


def apply_scm(repo_root, scm_key, build_cmd):
    for rel_path, content in SCMS[scm_key]["ci_files"](build_cmd).items():
        write(os.path.join(repo_root, rel_path), content)


def branch_readme(scm_key, build_key, pm_key, arch_key):
    scm = SCMS[scm_key]
    build = BUILD_TOOLS[build_key]
    pm = PACKAGE_MANAGERS[pm_key]
    arch_label = ARCHITECTURES[arch_key]
    branch_name = f"P1_{scm_key}_REACT_DOTNETCORE_{build_key}_{pm_key}_MVC_{arch_key}"

    ci_paths = {
        "GITHUB": ".github/workflows/ci.yml",
        "BITBUCKET": "bitbucket-pipelines.yml",
        "GITLAB": ".gitlab-ci.yml",
        "AZURE": "azure-pipelines.yml",
    }

    return f"""# record-platform-stack — {branch_name}

This branch is one cell of the **Project 1 / 9 Block** matrix — SCM x build
tool x package manager x architecture. All 96 branches in this matrix ship
the same ReactJS + ASP.NET Core + SQL Server application; they differ only
in the axes below.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| SCM                | {scm['label']} |
| Build tool         | {build['label']} |
| Package manager    | {pm['label']} |
| Architecture note  | {arch_label} |

> **Build tool note:** {build['note']}

> **Package manager note:** {pm['note']}

> **Architecture-note caveat:** like the rest of this corpus, "{arch_label}" is a
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
- **CI**: {scm['label']} (`{ci_paths[scm_key]}`), building the API with this
  branch's own build tool ({build['label']}) before building the client.

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
{build['build_cmd']}
cd RecordsApi && dotnet run

# client
cd ClientApp
npm ci
npm run dev
```
"""


def main():
    branches = []
    for scm_key in SCMS:
        for build_key in BUILD_TOOLS:
            for pm_key in PACKAGE_MANAGERS:
                for arch_key in ARCHITECTURES:
                    branches.append((scm_key, build_key, pm_key, arch_key))

    print(f"Generating {len(branches)} branches...")

    for scm_key, build_key, pm_key, arch_key in branches:
        branch_name = f"P1_{scm_key}_REACT_DOTNETCORE_{build_key}_{pm_key}_MVC_{arch_key}"
        print(f"--- {branch_name} ---")

        run(["git", "checkout", "--orphan", "tmp-p1-branch-build"])
        run(["git", "rm", "-rf", "--quiet", "."], check=False)
        for entry in os.listdir(REPO_ROOT):
            if entry == ".git":
                continue
            p = os.path.join(REPO_ROOT, entry)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)

        copy_template(TEMPLATE_DIR, REPO_ROOT)

        build_cmd = BUILD_TOOLS[build_key]["build_cmd"]
        apply_scm(REPO_ROOT, scm_key, build_cmd)
        apply_build_tool(REPO_ROOT, build_key)
        apply_package_manager(REPO_ROOT, pm_key)

        with open(os.path.join(REPO_ROOT, "README.md"), "w") as f:
            f.write(branch_readme(scm_key, build_key, pm_key, arch_key))

        run(["git", "add", "-A"])
        run(
            [
                "git",
                "commit",
                "-q",
                "-m",
                f"{branch_name}: {SCMS[scm_key]['label']} + {BUILD_TOOLS[build_key]['label']} + "
                f"{PACKAGE_MANAGERS[pm_key]['label']} + {ARCHITECTURES[arch_key]}",
            ]
        )
        run(["git", "branch", "-m", "tmp-p1-branch-build", branch_name])

    print("All 96 Project 1 branches generated.")


if __name__ == "__main__":
    main()
