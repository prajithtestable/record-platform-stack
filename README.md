# record-platform-stack

This repo hosts testbed reference stacks used to validate a code-scanning
platform against specific technology stacks. `main` holds only this README —
all runnable code lives on orphan branches (no shared git history with
`main` or with each other), one stack's worth of code per branch. Branches
differ **only** in bundler, package manager, and an architecture-note label;
none of that carries a `tools/` directory of tool-triggering fixtures, unlike
the per-language `*-Repos` corpora — these are build/bundler/package-manager
matrices only.

## Branch naming

`{LANG}_V{version}_{BUNDLER}_{PACKAGE_MANAGER}_{ARCHITECTURE}`, with an
optional project-name segment ahead of it when this repo hosts more than one
named stack — the convention already in use on the sibling
`javascript-combos` and `TypeScript-Repos` corpora (e.g.
`JS_V12_ESBUILD_NPM_MONO`), not the retired `CE-N{version}-{id}` scheme.

Three stacks currently live here:

| Stack | Branch prefix | Branches | Section |
| ----- | -------------- | -------- | ------- |
| record-platform-stack (Angular + Node microservices) | `JS_V22_*` | 24 | [below](#stack-record-platform-stack-js_v22) |
| Digital Sippoy (Next.js full-stack) | `DIGITAL_SIPPOY_JS_V20_*` | 24 | [below](#stack-digital-sippoy-digital_sippoy_js_v20) |
| Project 1 / 9 Block (React + ASP.NET Core + SQL Server) | `P1_*` | 96 | [below](#stack-project-1--9-block-p1_) |

The first two stacks share the same 3 bundlers × 4 package managers × 2
architecture-note grid (esbuild / Vite / Rollup × npm / yarn Berry / pnpm /
bun × Monolith / Microservices = 24 branches each), and both fixed the same
pnpm/yarn package-manager defects the same way — see each stack's own
"package-manager notes" section. Project 1 uses a different axis set (SCM ×
build tool × package manager × architecture) matched to its .NET backend —
see its own section for details, including an important verification caveat.

---

## Stack: record-platform-stack (`JS_V22_*`)

Modeled on
[`CE-Platform-Stack`](https://github.com/Mohammed-shihaf/CE-Platform-Stack).
It validates the platform against a microservices stack. Not a production
product — the business domain (a generic "record" entity) is intentionally
trivial. What matters is that every listed technology is genuinely present
and functional: real dependencies, real working code that runs end to end,
not stubs that merely claim to use a technology.

### Locked technology baseline

The same seven technologies are wired into every `JS_V22_*` branch,
unchanged:

- **Frontend**: Angular 20
- **Backend runtime**: Node.js 22
- **Database**: MongoDB 8
- **Search**: Elasticsearch 8
- **Queue**: SNS (`@aws-sdk/client-sns`, pointed at LocalStack — no real AWS credentials required to build or run)
- **Inter-service communication**: gRPC (`@grpc/grpc-js` + `@grpc/proto-loader`)
- **Email**: SES (`@aws-sdk/client-ses`, same LocalStack-mockable approach as SNS)

### Repository shape

Identical on every `JS_V22_*` branch:

```
/frontend                Angular 20 app — records page that calls the backend over HTTP/REST
/backend-service-a       Node.js 22 — gRPC server, owns MongoDB 8 (CRUD via mongoose)
/backend-service-b       Node.js 22 — gRPC client of service-a, owns Elasticsearch 8, SNS producer, SES sender
/shared/proto            .proto contract defining the gRPC service between service-a and service-b
docker-compose.yml       Mongo 8 + Elasticsearch 8 + LocalStack (SNS/SES)
```

**Flow**: the Angular frontend creates a "record" via service-a's REST
endpoint → service-a writes it to MongoDB and pushes it down a gRPC
server-streaming call (`WatchRecords`) that service-b is subscribed to →
service-b indexes the record into Elasticsearch, publishes an SNS
`record.created` event, and sends an SES notification email. gRPC also
exposes a unary `GetRecord` call, used by service-b for point lookups.

### Branch matrix (24 branches)

| Branch | Bundler | Package Manager | Architecture note |
| ------ | ------- | ---------------- | ------------------ |
| JS_V22_ESBUILD_NPM_MONO | esbuild (Angular's default Application Builder, `@angular/build`) | npm | Monolith |
| JS_V22_ESBUILD_NPM_MICRO | esbuild (Angular's default Application Builder, `@angular/build`) | npm | Microservices |
| JS_V22_ESBUILD_YARN_MONO | esbuild (Angular's default Application Builder, `@angular/build`) | yarn (Berry) | Monolith |
| JS_V22_ESBUILD_YARN_MICRO | esbuild (Angular's default Application Builder, `@angular/build`) | yarn (Berry) | Microservices |
| JS_V22_ESBUILD_PNPM_MONO | esbuild (Angular's default Application Builder, `@angular/build`) | pnpm | Monolith |
| JS_V22_ESBUILD_PNPM_MICRO | esbuild (Angular's default Application Builder, `@angular/build`) | pnpm | Microservices |
| JS_V22_ESBUILD_BUN_MONO | esbuild (Angular's default Application Builder, `@angular/build`) | bun | Monolith |
| JS_V22_ESBUILD_BUN_MICRO | esbuild (Angular's default Application Builder, `@angular/build`) | bun | Microservices |
| JS_V22_VITE_NPM_MONO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | npm | Monolith |
| JS_V22_VITE_NPM_MICRO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | npm | Microservices |
| JS_V22_VITE_YARN_MONO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | yarn (Berry) | Monolith |
| JS_V22_VITE_YARN_MICRO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | yarn (Berry) | Microservices |
| JS_V22_VITE_PNPM_MONO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | pnpm | Monolith |
| JS_V22_VITE_PNPM_MICRO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | pnpm | Microservices |
| JS_V22_VITE_BUN_MONO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | bun | Monolith |
| JS_V22_VITE_BUN_MICRO | Vite (esbuild used instead — not a real standalone Angular 20 bundler; see branch README) | bun | Microservices |
| JS_V22_ROLLUP_NPM_MONO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | npm | Monolith |
| JS_V22_ROLLUP_NPM_MICRO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | npm | Microservices |
| JS_V22_ROLLUP_YARN_MONO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | yarn (Berry) | Monolith |
| JS_V22_ROLLUP_YARN_MICRO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | yarn (Berry) | Microservices |
| JS_V22_ROLLUP_PNPM_MONO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | pnpm | Monolith |
| JS_V22_ROLLUP_PNPM_MICRO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | pnpm | Microservices |
| JS_V22_ROLLUP_BUN_MONO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | bun | Monolith |
| JS_V22_ROLLUP_BUN_MICRO | Rollup (esbuild used instead — not pluggable into Angular's CLI; see branch README) | bun | Microservices |

"Vite" and "Rollup" are not real independently-selectable Angular 20 CLI
bundlers — `ng build` only supports the esbuild-based Application Builder or
the legacy Webpack browser builder, and neither Vite nor Rollup has a
supported way to swap in as the underlying bundler. Every Vite- and
Rollup-labeled branch uses esbuild instead and documents that substitution
honestly in its own README, matching how `CE-Platform-Stack`'s `CE-A4`
branch handled the same situation. "Monolith" vs "Microservices" is a README
label only, consistent with the reference repo: every branch ships the same
`backend-service-a` / `backend-service-b` two-service code — the label
changes how the branch's use case is framed, not the code.

### Package-manager notes

- **pnpm 12** made previously-ignored build scripts fatal by default
  (`ERR_PNPM_IGNORED_BUILDS`). Every pnpm branch carries a
  `pnpm-workspace.yaml` with an `allowBuilds:` map (`protobufjs` for both
  backend services; `@parcel/watcher`, `esbuild`, `lmdb`, `msgpackr-extract`
  for the frontend's Angular CLI toolchain) so `pnpm install
  --frozen-lockfile` succeeds from a clean checkout.
- **pnpm's and yarn's minimum-release-age policies** both reject lockfile
  entries published very recently by default (pnpm: `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION`;
  yarn: package "quarantine"). Both are set to `0` in this repo
  (`minimumReleaseAge: 0` in `pnpm-workspace.yaml`, `npmMinimalAgeGate: 0` in
  `.yarnrc.yml`) since the AWS SDK v3 clients here were resolved same-day.
- **yarn Berry** branches vendor the actual CLI at
  `.yarn/releases/yarn-4.18.0.cjs` (from the official `@yarnpkg/cli-dist` npm
  package) with `nodeLinker: node-modules`, so `yarn install --immutable`
  works standalone without a network call to `repo.yarnpkg.com`.
- All four package managers (`npm ci`, `yarn install --immutable`, `pnpm
  install --frozen-lockfile`, `bun install --frozen-lockfile`) were verified
  to install from their committed lockfile, and the Angular frontend was
  verified to build under all four, before any branch was generated.

### Generator

`_generator/generate_branches.py` is parameterised (bundlers, package
managers, architectures, per-branch README template) and regenerates the
full 24-branch matrix from a template directory plus a pre-verified
lockfile-set store. Retarget by editing the `BUNDLERS` / `PACKAGE_MANAGERS`
/ `ARCHITECTURES` dicts at the top of the script.

---

## Stack: Digital Sippoy (`DIGITAL_SIPPOY_JS_V20_*`)

A second, single-app stack in this same repo — full-stack Next.js only, no
separate backend services and no database/queue/search/email layer. Same
testbed intent as record-platform-stack: real dependencies, real working
code, nothing stubbed.

### Locked technology baseline

- **Runtime**: Node.js 20
- **Framework**: Next.js 15.5.12 (App Router)
- **UI library**: React 19.1.0 / react-dom 19.1.0

### Repository shape

Identical on every `DIGITAL_SIPPOY_JS_V20_*` branch:

```
/app                  Next.js App Router: page.tsx, layout.tsx, globals.css
/app/actions.ts        Server Actions (create/delete), used directly by the page
/app/api/records        Route Handlers (GET/POST) — a genuine REST surface
/app/api/records/[id]   Route Handlers (GET/DELETE) for a single record
/lib/records-store.ts   In-memory records store shared by actions and route handlers
Dockerfile              Multi-stage build using Next's standalone output
docker-compose.yml       Single `app` service, port 3000
```

**Flow**: the homepage is a Server Component that reads the in-memory store
directly and renders a table plus a form. The form posts through a React 19
`useActionState`-bound Server Action, which mutates the store and
revalidates the page. `/api/records` and `/api/records/[id]` expose the same
store as a conventional REST API for external callers, independent of the
page's Server Action path.

### Branch matrix (24 branches)

| Branch | Bundler | Package Manager | Architecture note |
| ------ | ------- | ---------------- | ------------------ |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_NPM_MONO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Monolith |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_NPM_MICRO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Microservices |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_YARN_MONO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Monolith |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_YARN_MICRO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Microservices |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_PNPM_MONO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Monolith |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_PNPM_MICRO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Microservices |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_BUN_MONO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Monolith |
| DIGITAL_SIPPOY_JS_V20_ESBUILD_BUN_MICRO | esbuild (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Microservices |
| DIGITAL_SIPPOY_JS_V20_VITE_NPM_MONO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Monolith |
| DIGITAL_SIPPOY_JS_V20_VITE_NPM_MICRO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Microservices |
| DIGITAL_SIPPOY_JS_V20_VITE_YARN_MONO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Monolith |
| DIGITAL_SIPPOY_JS_V20_VITE_YARN_MICRO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Microservices |
| DIGITAL_SIPPOY_JS_V20_VITE_PNPM_MONO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Monolith |
| DIGITAL_SIPPOY_JS_V20_VITE_PNPM_MICRO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Microservices |
| DIGITAL_SIPPOY_JS_V20_VITE_BUN_MONO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Monolith |
| DIGITAL_SIPPOY_JS_V20_VITE_BUN_MICRO | Vite (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Microservices |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_NPM_MONO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Monolith |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_NPM_MICRO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | npm | Microservices |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_YARN_MONO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Monolith |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_YARN_MICRO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | yarn (Berry) | Microservices |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_PNPM_MONO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Monolith |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_PNPM_MICRO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | pnpm | Microservices |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_BUN_MONO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Monolith |
| DIGITAL_SIPPOY_JS_V20_ROLLUP_BUN_MICRO | Rollup (Next.js's own default `next build` tool — Webpack — used instead; see branch README) | bun | Microservices |

None of esbuild, Vite, or Rollup are pluggable into `next build` — Next.js
15.5.12 has its own build pipeline (Webpack by default; Turbopack as an
opt-in alternative via `next build --turbopack`, neither of which is
esbuild/Vite/Rollup). Every branch runs Next's real default (Webpack) and
documents the label substitution honestly, the same way the record-platform-
stack matrix handles Vite/Rollup for Angular. "Monolith" vs "Microservices"
is a label only here too — there's no separate backend service to split out
in a full-stack Next.js app, so every branch ships the identical single app.

### Package-manager notes

Same defect classes as record-platform-stack, hit again on this stack's
dependency set:

- **pnpm**: `sharp` (an optional Next.js image-optimization dependency) needed
  a build-script approval — `pnpm-workspace.yaml` carries `allowBuilds:
  sharp: true` plus `minimumReleaseAge: 0`.
- **yarn Berry**: same vendored `.yarn/releases/yarn-4.18.0.cjs` +
  `nodeLinker: node-modules` + `npmMinimalAgeGate: 0` approach. `sharp`'s
  build script is left disabled under yarn's own scripts-off-by-default
  policy — harmless here since this app never imports `next/image`/`sharp`.
- All four package managers were verified with a real `next build` under the
  actual Node 20.20.2 binary (not just Node 22 with an `engines` pin) before
  any branch was generated.

### Running any branch

```bash
git checkout <branch-name>
docker compose up --build
```

or install/run locally with that branch's package manager — see the
branch's own README for exact commands.

### Generator

`_generator/generate_sippoy_branches.py`, same shape as
`generate_branches.py` — parameterised bundlers/package
managers/architectures, regenerates the 24-branch matrix from a template
directory plus a pre-verified lockfile-set store.

---

## Stack: Project 1 / 9 Block (`P1_*`)

A third, independent stack in this same repo, modeled on a different tech
spec: "9 Block" — SCM (GitHub / Bitbucket / GitLab / Azure) x React frontend
x ASP.NET Core + SQL Server backend x MVC development style. Same testbed
intent as the other two stacks: real dependencies, real working code, not
stubs — with one caveat, see "Verification status" below.

### Locked technology baseline

- **Frontend**: ReactJS (Vite-based dev/build tooling)
- **Backend**: ASP.NET Core 8 Web API
- **Database**: SQL Server 2022 (via EF Core, `Microsoft.EntityFrameworkCore.SqlServer`)
- **Development style**: "Entire Architecture (Model, View, Controller)" —
  Model and Controller are the EF Core entities and ASP.NET Core controllers
  in `RecordsApi`; View is realized as the separately-served React SPA in
  `ClientApp` rather than Razor views, since this is an API + SPA pairing
  rather than a server-rendered MVC app. Documented per-branch rather than
  silently assumed.

### Repository shape

Identical on every `P1_*` branch:

```
/ClientApp               React (Vite) app — Records list/add/delete UI, calls RecordsApi over HTTP
/RecordsApi               ASP.NET Core 8 Web API — Records CRUD controller, EF Core DbContext, SQL Server
docker-compose.yml        SQL Server 2022 + RecordsApi + ClientApp (nginx-served build)
```

**Flow**: the React SPA calls `RecordsApi`'s `/api/records` endpoints
(GET/POST/PUT/DELETE) → `RecordsController` uses `AppDbContext` (EF Core) to
read/write the `Records` table in SQL Server, creating the schema on startup
via `EnsureCreated()`.

### Branch matrix (96 branches)

4 SCMs × 3 build tools × 4 package managers × 2 architecture-note labels.

| Branch | SCM | Build Tool | Package Manager | Architecture note |
| ------ | --- | ---------- | ---------------- | ------------------ |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MONO | GitHub | SDK-style MSBuild | NuGet (PackageReference) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MICRO | GitHub | SDK-style MSBuild | NuGet (PackageReference) | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MONO | GitHub | SDK-style MSBuild | Central Package Management | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MICRO | GitHub | SDK-style MSBuild | Central Package Management | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MONO | GitHub | SDK-style MSBuild | Paket | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MICRO | GitHub | SDK-style MSBuild | Paket | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MONO | GitHub | SDK-style MSBuild | NuGet (packages.config) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MICRO | GitHub | SDK-style MSBuild | NuGet (packages.config) | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MONO | GitHub | Cake | NuGet (PackageReference) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MICRO | GitHub | Cake | NuGet (PackageReference) | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_CPM_MVC_MONO | GitHub | Cake | Central Package Management | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_CPM_MVC_MICRO | GitHub | Cake | Central Package Management | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_PAKET_MVC_MONO | GitHub | Cake | Paket | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_PAKET_MVC_MICRO | GitHub | Cake | Paket | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MONO | GitHub | Cake | NuGet (packages.config) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MICRO | GitHub | Cake | NuGet (packages.config) | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MONO | GitHub | .NET CLI | NuGet (PackageReference) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MICRO | GitHub | .NET CLI | NuGet (PackageReference) | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CLI_CPM_MVC_MONO | GitHub | .NET CLI | Central Package Management | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CLI_CPM_MVC_MICRO | GitHub | .NET CLI | Central Package Management | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CLI_PAKET_MVC_MONO | GitHub | .NET CLI | Paket | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CLI_PAKET_MVC_MICRO | GitHub | .NET CLI | Paket | Microservices |
| P1_GITHUB_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MONO | GitHub | .NET CLI | NuGet (packages.config) | Monolith |
| P1_GITHUB_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MICRO | GitHub | .NET CLI | NuGet (packages.config) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MONO | Bitbucket | SDK-style MSBuild | NuGet (PackageReference) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MICRO | Bitbucket | SDK-style MSBuild | NuGet (PackageReference) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MONO | Bitbucket | SDK-style MSBuild | Central Package Management | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MICRO | Bitbucket | SDK-style MSBuild | Central Package Management | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MONO | Bitbucket | SDK-style MSBuild | Paket | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MICRO | Bitbucket | SDK-style MSBuild | Paket | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MONO | Bitbucket | SDK-style MSBuild | NuGet (packages.config) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MICRO | Bitbucket | SDK-style MSBuild | NuGet (packages.config) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MONO | Bitbucket | Cake | NuGet (PackageReference) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MICRO | Bitbucket | Cake | NuGet (PackageReference) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_CPM_MVC_MONO | Bitbucket | Cake | Central Package Management | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_CPM_MVC_MICRO | Bitbucket | Cake | Central Package Management | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_PAKET_MVC_MONO | Bitbucket | Cake | Paket | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_PAKET_MVC_MICRO | Bitbucket | Cake | Paket | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MONO | Bitbucket | Cake | NuGet (packages.config) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MICRO | Bitbucket | Cake | NuGet (packages.config) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MONO | Bitbucket | .NET CLI | NuGet (PackageReference) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MICRO | Bitbucket | .NET CLI | NuGet (PackageReference) | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_CPM_MVC_MONO | Bitbucket | .NET CLI | Central Package Management | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_CPM_MVC_MICRO | Bitbucket | .NET CLI | Central Package Management | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_PAKET_MVC_MONO | Bitbucket | .NET CLI | Paket | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_PAKET_MVC_MICRO | Bitbucket | .NET CLI | Paket | Microservices |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MONO | Bitbucket | .NET CLI | NuGet (packages.config) | Monolith |
| P1_BITBUCKET_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MICRO | Bitbucket | .NET CLI | NuGet (packages.config) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MONO | GitLab | SDK-style MSBuild | NuGet (PackageReference) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MICRO | GitLab | SDK-style MSBuild | NuGet (PackageReference) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MONO | GitLab | SDK-style MSBuild | Central Package Management | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MICRO | GitLab | SDK-style MSBuild | Central Package Management | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MONO | GitLab | SDK-style MSBuild | Paket | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MICRO | GitLab | SDK-style MSBuild | Paket | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MONO | GitLab | SDK-style MSBuild | NuGet (packages.config) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MICRO | GitLab | SDK-style MSBuild | NuGet (packages.config) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MONO | GitLab | Cake | NuGet (PackageReference) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MICRO | GitLab | Cake | NuGet (PackageReference) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_CPM_MVC_MONO | GitLab | Cake | Central Package Management | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_CPM_MVC_MICRO | GitLab | Cake | Central Package Management | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_PAKET_MVC_MONO | GitLab | Cake | Paket | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_PAKET_MVC_MICRO | GitLab | Cake | Paket | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MONO | GitLab | Cake | NuGet (packages.config) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MICRO | GitLab | Cake | NuGet (packages.config) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MONO | GitLab | .NET CLI | NuGet (PackageReference) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MICRO | GitLab | .NET CLI | NuGet (PackageReference) | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CLI_CPM_MVC_MONO | GitLab | .NET CLI | Central Package Management | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CLI_CPM_MVC_MICRO | GitLab | .NET CLI | Central Package Management | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CLI_PAKET_MVC_MONO | GitLab | .NET CLI | Paket | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CLI_PAKET_MVC_MICRO | GitLab | .NET CLI | Paket | Microservices |
| P1_GITLAB_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MONO | GitLab | .NET CLI | NuGet (packages.config) | Monolith |
| P1_GITLAB_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MICRO | GitLab | .NET CLI | NuGet (packages.config) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MONO | Azure DevOps | SDK-style MSBuild | NuGet (PackageReference) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_NUGETPKGREF_MVC_MICRO | Azure DevOps | SDK-style MSBuild | NuGet (PackageReference) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MONO | Azure DevOps | SDK-style MSBuild | Central Package Management | Monolith |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_CPM_MVC_MICRO | Azure DevOps | SDK-style MSBuild | Central Package Management | Microservices |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MONO | Azure DevOps | SDK-style MSBuild | Paket | Monolith |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_PAKET_MVC_MICRO | Azure DevOps | SDK-style MSBuild | Paket | Microservices |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MONO | Azure DevOps | SDK-style MSBuild | NuGet (packages.config) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_MSBUILD_NUGETCONFIG_MVC_MICRO | Azure DevOps | SDK-style MSBuild | NuGet (packages.config) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MONO | Azure DevOps | Cake | NuGet (PackageReference) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CAKE_NUGETPKGREF_MVC_MICRO | Azure DevOps | Cake | NuGet (PackageReference) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CAKE_CPM_MVC_MONO | Azure DevOps | Cake | Central Package Management | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CAKE_CPM_MVC_MICRO | Azure DevOps | Cake | Central Package Management | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CAKE_PAKET_MVC_MONO | Azure DevOps | Cake | Paket | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CAKE_PAKET_MVC_MICRO | Azure DevOps | Cake | Paket | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MONO | Azure DevOps | Cake | NuGet (packages.config) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CAKE_NUGETCONFIG_MVC_MICRO | Azure DevOps | Cake | NuGet (packages.config) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MONO | Azure DevOps | .NET CLI | NuGet (PackageReference) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CLI_NUGETPKGREF_MVC_MICRO | Azure DevOps | .NET CLI | NuGet (PackageReference) | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CLI_CPM_MVC_MONO | Azure DevOps | .NET CLI | Central Package Management | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CLI_CPM_MVC_MICRO | Azure DevOps | .NET CLI | Central Package Management | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CLI_PAKET_MVC_MONO | Azure DevOps | .NET CLI | Paket | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CLI_PAKET_MVC_MICRO | Azure DevOps | .NET CLI | Paket | Microservices |
| P1_AZURE_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MONO | Azure DevOps | .NET CLI | NuGet (packages.config) | Monolith |
| P1_AZURE_REACT_DOTNETCORE_CLI_NUGETCONFIG_MVC_MICRO | Azure DevOps | .NET CLI | NuGet (packages.config) | Microservices |

The SCM axis isn't label-only: each branch ships that platform's own CI
config at the repo root (`.github/workflows/ci.yml`, `bitbucket-pipelines.yml`,
`.gitlab-ci.yml`, or `azure-pipelines.yml`), and that config's build step
invokes the branch's own build-tool command (e.g. the GitLab+Cake branch's
`.gitlab-ci.yml` runs `dotnet cake RecordsApi/build.cake --target=Build`,
while the GitHub+MSBuild branch's `ci.yml` runs
`dotnet msbuild RecordsApi/RecordsApi.csproj -restore`).

"Monolith" vs "Microservices" is a label only here too, same as the other
two stacks in this repo — every branch ships the identical single
`RecordsApi` service; the architecture note doesn't change the code, only
how the branch's own README frames it.

### Package-manager notes

- **NuGet (PackageReference)**: the SDK-style default — `<PackageReference>`
  items with explicit `Version` attributes in `RecordsApi.csproj`.
- **Central Package Management**: a root `Directory.Packages.props` centralizes
  versions (`ManagePackageVersionsCentrally=true`); `RecordsApi.csproj` lists
  `<PackageReference>` items with no `Version` attribute.
- **Paket**: a root `paket.dependencies` + `RecordsApi/paket.references`,
  imported via `.paket/Paket.Restore.targets`.
- **NuGet (packages.config)**: **substitution note** — `packages.config` is
  not supported by SDK-style projects (`net8.0`, `Microsoft.NET.Sdk.Web`);
  it's a legacy mechanism for non-SDK, `.NET Framework`-style `.csproj`
  files only. This branch honestly keeps `PackageReference` (identical to
  the NuGet (PackageReference) branch) and documents the substitution
  rather than shipping a `packages.config` that .NET 8 would ignore.

### Build-tool notes

- **SDK-style MSBuild**: invoked directly via `dotnet msbuild` against the
  SDK-style `.csproj`.
- **Cake**: driven by `RecordsApi/build.cake` via the local `Cake.Tool` .NET
  tool declared in `.config/dotnet-tools.json`.
- **.NET CLI**: the plain `dotnet build`/`dotnet run` workflow, with the SDK
  version pinned via a root `global.json`.

### Verification status

Unlike the other two stacks in this repo, this one was **not** fully
build-verified. It was authored in a sandbox that could reach npm's
registry but could **not** reach `nuget.org` (proxy returned 403 on every
NuGet request). As a result:

- **`ClientApp` (React/Vite) — verified.** `npm install` and `npm run build`
  both completed successfully, on the template and on a spot-checked
  generated branch.
- **`RecordsApi` (.NET/EF Core/SQL Server) — unverified.** `dotnet restore`
  could not complete (no NuGet access), so `dotnet build` could not be run.
  The C# source, `.csproj` files, and package-manager/build-tool
  configuration were written correctly from knowledge, following standard
  ASP.NET Core 8 + EF Core + SQL Server patterns, but have not been
  compiled in this environment. They should build normally wherever
  `nuget.org` is reachable.

Every branch's own README repeats this note under "Verification note" so
it isn't lost when browsing a single branch in isolation.

### Running any branch

```bash
git checkout <branch-name>
docker compose up --build
```

or run the API and client locally — see the branch's own README for exact
commands.

### Generator

`_generator/generate_project1_branches.py` — parameterised SCM/build
tool/package manager/architecture, regenerates the 96-branch matrix from a
template directory (`ClientApp/` + `RecordsApi/` + `docker-compose.yml` +
`.gitignore`).
