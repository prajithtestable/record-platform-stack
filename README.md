# record-platform-stack — JS_V22_ESBUILD_BUN_MONO

This branch is one cell of the record-platform-stack bundler x package-manager x
architecture matrix. All 24 branches ship the exact same application code —
they differ **only** in bundler, package manager, and this README's
architecture-note label.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| Bundler            | esbuild |
| Package manager    | bun |
| Architecture note  | Monolith |

> **Architecture-note caveat:** like the rest of this matrix, "Monolith" is a
> label only. Every branch ships the same `backend-service-a` / `backend-service-b`
> two-service layout described in the root `main` README — the architecture note
> does not change the code, only how this branch's use case is framed.

## Locked technology baseline

- **Frontend**: Angular 20
- **Backend runtime**: Node.js 22
- **Database**: MongoDB 8
- **Search**: Elasticsearch 8
- **Queue**: SNS (`@aws-sdk/client-sns`, pointed at LocalStack)
- **Inter-service communication**: gRPC (`@grpc/grpc-js` + `@grpc/proto-loader`)
- **Email**: SES (`@aws-sdk/client-ses`, same LocalStack-mockable approach as SNS)

## Repository shape

```
/frontend                Angular 20 app — records page that calls service-a over HTTP/REST
/backend-service-a       Node.js 22 — gRPC server, owns MongoDB 8 (CRUD via mongoose)
/backend-service-b       Node.js 22 — gRPC client of service-a, owns Elasticsearch 8, SNS producer, SES sender
/shared/proto            .proto contract defining the gRPC service between service-a and service-b
docker-compose.yml       Mongo 8 + Elasticsearch 8 + LocalStack (SNS/SES)
```

**Flow**: the Angular frontend creates a record via service-a's REST endpoint
→ service-a writes it to MongoDB and pushes it down a gRPC server-streaming
call (`WatchRecords`) that service-b is subscribed to → service-b indexes the
record into Elasticsearch, publishes an SNS `record.created` event, and sends
an SES notification email.

## Running this branch

Fastest path — everything in containers:

```bash
docker compose up --build
```

Or run each piece locally with bun:

```bash
# backend-service-a
cd backend-service-a && bun install --frozen-lockfile && bun run start

# backend-service-b (needs Elasticsearch + LocalStack reachable)
cd backend-service-b && bun install --frozen-lockfile && bun run start

# frontend
cd frontend && bun install --frozen-lockfile && bun run start
```

Production build of the frontend: `bun run build` (run inside `frontend/`).
