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

Two stacks currently live here:

| Stack | Branch prefix | Branches | Section |
| ----- | -------------- | -------- | ------- |
| record-platform-stack (Angular + Node microservices) | `JS_V22_*` | 24 | [below](#stack-record-platform-stack-js_v22) |
| Digital Sippoy (Next.js full-stack) | `DIGITAL_SIPPOY_JS_V20_*` | 24 | [below](#stack-digital-sippoy-digital_sippoy_js_v20) |

Both stacks share the same 3 bundlers × 4 package managers × 2
architecture-note grid (esbuild / Vite / Rollup × npm / yarn Berry / pnpm /
bun × Monolith / Microservices = 24 branches each), and both fixed the same
pnpm/yarn package-manager defects the same way — see each stack's own
"package-manager notes" section.

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
