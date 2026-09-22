# Digital Sippoy — DIGITAL_SIPPOY_JS_V20_ESBUILD_NPM_MICRO

This branch is one cell of the Digital Sippoy bundler x package-manager x
architecture matrix, living in the same repo as the record-platform-stack
(`JS_V22_*`) matrix. All 24 `DIGITAL_SIPPOY_JS_V20_*` branches ship the exact
same application code — they differ **only** in bundler, package manager,
and this README's architecture-note label.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| Bundler            | esbuild |
| Package manager    | npm |
| Architecture note  | Microservices |

> **Bundler substitution note:** Next.js's own default build tool is used instead (Webpack, the `next build` default in Next.js 15.5.12). esbuild is not a pluggable bundler for `next build` — Next.js's build pipeline is not built on esbuild the way Angular's Application Builder is, so there is no supported way to select it here. This branch documents the substitution honestly rather than mislabeling Webpack output as esbuild.

> **Architecture-note caveat:** "Microservices" is a label only. Every branch
> ships the same single Next.js application — the architecture note does not
> change the code, only how this branch's use case is framed. (This stack is
> full-stack-only: there is no separate backend service to split out the way
> record-platform-stack's `backend-service-a`/`backend-service-b` are.)

## Locked technology baseline

- **Runtime**: Node.js 20
- **Framework**: Next.js 15.5.12 (App Router)
- **UI library**: React 19.1.0 / react-dom 19.1.0

No external database, queue, search, or email service is part of this
stack — "records" are held in an in-memory store for the lifetime of the
Node process. Real CRUD, real Server Actions, real Route Handlers; nothing
here is a stub.

## Repository shape

```
/app                  Next.js App Router: page.tsx, layout.tsx, globals.css
/app/actions.ts        Server Actions (create/delete), used directly by the page
/app/api/records        Route Handlers (GET/POST) — a genuine REST surface
/app/api/records/[id]   Route Handlers (GET/DELETE) for a single record
/lib/records-store.ts   In-memory records store shared by actions and route handlers
Dockerfile              Multi-stage build using Next's standalone output
docker-compose.yml       Single `app` service, port 3000
```

**Flow**: the homepage is a Server Component that reads the store directly
and renders a table plus a form. The form posts through a React 19
`useActionState`-bound Server Action (`createRecordAction`), which mutates
the store and revalidates the page. `/api/records` and `/api/records/[id]`
expose the same store as a conventional REST API for external callers,
independent of the page's Server Action path.

## Running this branch

Fastest path — container:

```bash
docker compose up --build
```

Or locally with npm (Node 20 required):

```bash
npm ci
npm run dev      # dev server
npm run build    # production build
npm start      # after building
```
