#!/usr/bin/env python3
"""
Generates the JS_V22_<BUNDLER>_<PKGMGR>_<ARCH> branch matrix for
record-platform-stack, following the same naming convention as the
sibling javascript-combos / TypeScript-Repos / python-grid corpora:

    {LANG}_V{version}_{BUNDLER}_{PACKAGE_MANAGER}_{ARCHITECTURE}

Fixed here at Node 22 (the locked runtime for this stack), so every
branch is JS_V22_*. 3 bundlers x 4 package managers x 2 architectures
= 24 branches. Each branch is an orphan branch (no shared history with
main) carrying the full, byte-identical application code plus the
lockfile set for its own package manager and a branch-specific README.

This script expects two inputs that are NOT part of this repo (kept
out on purpose, same as the sibling corpora keep large generator state
outside the shipped tree):

  TEMPLATE_DIR   a clean copy of frontend/, backend-service-a/,
                 backend-service-b/, shared/, docker-compose.yml,
                 .gitignore (no node_modules/dist/.angular/lockfiles)
  LOCKFILE_SETS  <pm>/<project>/<lockfile files> for pm in
                 npm|yarn|pnpm|bun and project in
                 frontend|backend-service-a|backend-service-b,
                 each verified to install with a frozen/immutable
                 lockfile (npm ci / yarn install --immutable /
                 pnpm install --frozen-lockfile / bun install
                 --frozen-lockfile) before being folded in here.

  yarn sets use a vendored `.yarn/releases/yarn-<ver>.cjs` (from the
  npm-published `@yarnpkg/cli-dist` package) plus `.yarnrc.yml` with
  `nodeLinker: node-modules` and `npmMinimalAgeGate: 0`.

  pnpm sets carry a `pnpm-workspace.yaml` with an `allowBuilds:` map
  (pnpm 12 made previously-ignored build scripts fatal by default —
  see ERR_PNPM_IGNORED_BUILDS) and `minimumReleaseAge: 0` (pnpm's
  supply-chain policy otherwise rejects lockfile entries published
  very recently, e.g. same-day AWS SDK releases).

Usage: python3 _generator/generate_branches.py
Run from the repo root, on a clean working tree.
"""
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKFILE_SETS = os.environ.get("LOCKFILE_SETS", "/tmp/lockfile-sets")
TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", "/tmp/branch-template")

BUNDLERS = {
    "ESBUILD": {
        "label": "esbuild",
        "detail": "Angular's default Application Builder (`@angular/build`, `@angular/build:application`). "
        "This is a real, independently-selectable Angular 20 build backend.",
        "substitution": None,
    },
    "VITE": {
        "label": "Vite",
        "detail": "esbuild is used in its place. Vite is **not** a real standalone Angular 20 CLI bundler — "
        "Angular's esbuild Application Builder uses Vite internally only for its dev-server "
        "(`ng serve`), never for `ng build`. There is no `@angular-builders` or first-party "
        "config that swaps Vite in as the production bundler, so this branch honestly ships "
        "the esbuild Application Builder and documents the substitution here rather than "
        "silently mislabeling esbuild output as \"Vite\".",
        "substitution": "esbuild",
    },
    "ROLLUP": {
        "label": "Rollup",
        "detail": "esbuild is used in its place. Rollup is likewise not a pluggable bundler for Angular 20's "
        "CLI: `ng build` only accepts the esbuild-based Application Builder or the legacy "
        "Webpack browser builder (`@angular-devkit/build-angular:browser`) — neither has a "
        "supported way to swap in Rollup as the underlying bundler. This branch ships the "
        "esbuild Application Builder and documents the substitution honestly, the same way "
        "the Vite-labeled branches in this matrix do.",
        "substitution": "esbuild",
    },
}

PACKAGE_MANAGERS = {
    "NPM": {
        "label": "npm",
        "install": "npm ci",
        "run_frontend": "npm start",
        "run_backend": "npm start",
        "build_frontend": "npm run build",
    },
    "YARN": {
        "label": "yarn (Berry)",
        "install": "yarn install --immutable",
        "run_frontend": "yarn start",
        "run_backend": "yarn start",
        "build_frontend": "yarn build",
    },
    "PNPM": {
        "label": "pnpm",
        "install": "pnpm install --frozen-lockfile",
        "run_frontend": "pnpm start",
        "run_backend": "pnpm start",
        "build_frontend": "pnpm build",
    },
    "BUN": {
        "label": "bun",
        "install": "bun install --frozen-lockfile",
        "run_frontend": "bun run start",
        "run_backend": "bun run start",
        "build_frontend": "bun run build",
    },
}

ARCHITECTURES = {
    "MONO": "Monolith",
    "MICRO": "Microservices",
}

ALL_LOCKFILE_NAMES = [
    "package-lock.json",
    "yarn.lock",
    ".yarnrc.yml",
    ".yarn",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
    "bun.lock",
]


def run(cmd, cwd=REPO_ROOT, check=True):
    result = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"FAILED: {cmd}\n{result.stdout}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result


def clear_lockfiles(project_dir):
    for name in ALL_LOCKFILE_NAMES:
        p = os.path.join(project_dir, name)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)


def install_lockfiles(project_dir, project_key, pm):
    src_dir = os.path.join(LOCKFILE_SETS, pm.lower(), project_key)
    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(project_dir, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def branch_readme(bundler_key, pm_key, arch_key):
    bundler = BUNDLERS[bundler_key]
    pm = PACKAGE_MANAGERS[pm_key]
    arch_label = ARCHITECTURES[arch_key]
    branch_name = f"JS_V22_{bundler_key}_{pm_key}_{arch_key}"

    substitution_note = ""
    if bundler["substitution"]:
        substitution_note = f"\n> **Bundler substitution note:** {bundler['detail']}\n"

    return f"""# record-platform-stack — {branch_name}

This branch is one cell of the record-platform-stack bundler x package-manager x
architecture matrix. All 24 branches ship the exact same application code —
they differ **only** in bundler, package manager, and this README's
architecture-note label.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| Bundler            | {bundler['label']} |
| Package manager    | {pm['label']} |
| Architecture note  | {arch_label} |
{substitution_note}
> **Architecture-note caveat:** like the rest of this matrix, "{arch_label}" is a
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

Or run each piece locally with {pm['label']}:

```bash
# backend-service-a
cd backend-service-a && {pm['install']} && {pm['run_backend']}

# backend-service-b (needs Elasticsearch + LocalStack reachable)
cd backend-service-b && {pm['install']} && {pm['run_backend']}

# frontend
cd frontend && {pm['install']} && {pm['run_frontend']}
```

Production build of the frontend: `{pm['build_frontend']}` (run inside `frontend/`).
"""


def main():
    branches = []
    for bundler_key in BUNDLERS:
        for pm_key in PACKAGE_MANAGERS:
            for arch_key in ARCHITECTURES:
                branches.append((bundler_key, pm_key, arch_key))

    print(f"Generating {len(branches)} branches...")

    for bundler_key, pm_key, arch_key in branches:
        branch_name = f"JS_V22_{bundler_key}_{pm_key}_{arch_key}"
        print(f"--- {branch_name} ---")

        run(["git", "checkout", "--orphan", "tmp-branch-build"])
        run(["git", "rm", "-rf", "--quiet", "."], check=False)
        for entry in os.listdir(REPO_ROOT):
            if entry == ".git":
                continue
            p = os.path.join(REPO_ROOT, entry)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)

        for entry in os.listdir(TEMPLATE_DIR):
            src = os.path.join(TEMPLATE_DIR, entry)
            dst = os.path.join(REPO_ROOT, entry)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        clear_lockfiles(os.path.join(REPO_ROOT, "frontend"))
        install_lockfiles(os.path.join(REPO_ROOT, "frontend"), "frontend", pm_key)
        for svc in ["backend-service-a", "backend-service-b"]:
            clear_lockfiles(os.path.join(REPO_ROOT, svc))
            install_lockfiles(os.path.join(REPO_ROOT, svc), svc, pm_key)

        with open(os.path.join(REPO_ROOT, "README.md"), "w") as f:
            f.write(branch_readme(bundler_key, pm_key, arch_key))

        run(["git", "add", "-A"])
        run(
            [
                "git",
                "commit",
                "-q",
                "-m",
                f"{branch_name}: {BUNDLERS[bundler_key]['label']} + "
                f"{PACKAGE_MANAGERS[pm_key]['label']} + {ARCHITECTURES[arch_key]}",
            ]
        )
        run(["git", "branch", "-m", "tmp-branch-build", branch_name])

    print("All branches generated.")


if __name__ == "__main__":
    main()
