# record-platform-stack

record-platform-stack is a testbed reference repository, built after the
`testable-platform` per-language corpus consolidation and modeled on
[`CE-Platform-Stack`](https://github.com/Mohammed-shihaf/CE-Platform-Stack).
It validates a code-scanning platform against a specific microservices
technology stack. It is not a production product — the business domain (a
generic "record" entity) is intentionally trivial. What matters is that every
listed technology is genuinely present and functional: real dependencies,
real working code that runs end to end, not stubs that merely claim to use a
technology. Unlike the per-language `*-Repos` corpora this repo does not carry
a `tools/` directory of tool-triggering fixtures — it is a build/bundler/
package-manager matrix only.

## Locked technology baseline

The same seven technologies are wired into every branch, unchanged:

- **Frontend**: Angular 20
- **Backend runtime**: Node.js 22
- **Database**: MongoDB 8
- **Search**: Elasticsearch 8
- **Queue**: SNS (`@aws-sdk/client-sns`, pointed at LocalStack — no real AWS credentials required to build or run)
- **Inter-service communication**: gRPC (`@grpc/grpc-js` + `@grpc/proto-loader`)
- **Email**: SES (`@aws-sdk/client-ses`, same LocalStack-mockable approach as SNS)

## Repository shape

Identical on every branch:

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

## Branch naming

`{LANG}_V{version}_{BUNDLER}_{PACKAGE_MANAGER}_{ARCHITECTURE}` — the same
convention already in use on the sibling `javascript-combos` and
`TypeScript-Repos` corpora (e.g. `JS_V12_ESBUILD_NPM_MONO`), not the retired
`CE-N{version}-{id}` scheme. The runtime here is fixed at Node 22, so every
branch is `JS_V22_*`.

`main` holds only this README. All runnable code lives on the 24 `JS_V22_*`
branches below — each is an **orphan branch** (no shared git history with
`main` or with each other), carrying the full, byte-identical application
code plus the lockfile set for its own package manager. Branches differ
**only** in bundler, package manager, and the architecture-note label in
that branch's own README.

## Branch matrix (24 branches — 3 bundlers × 4 package managers × 2 architectures)

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

## Package-manager notes (found while building this corpus)

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

## Running any branch

```bash
git checkout <branch-name>
docker compose up --build
```

or install/run each piece locally with that branch's package manager — see
the branch's own README for exact commands.

## Generator

`_generator/generate_branches.py` is parameterised (bundlers, package
managers, architectures, per-branch README template) and regenerates the
full 24-branch matrix from a template directory plus a pre-verified
lockfile-set store. Retarget by editing the `BUNDLERS` / `PACKAGE_MANAGERS`
/ `ARCHITECTURES` dicts at the top of the script.
