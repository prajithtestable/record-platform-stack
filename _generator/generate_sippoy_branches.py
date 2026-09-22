#!/usr/bin/env python3
"""
Generates the DIGITAL_SIPPOY_JS_V20_<BUNDLER>_<PKGMGR>_<ARCH> branch matrix
in this same repo, alongside the JS_V22_* record-platform-stack branches.
Same naming convention, same 3 x 4 x 2 = 24 grid, different stack:

    Digital Sippoy — Next.js 15.5.12 / React 19.1.0, Node.js 20, full-stack
    only (no separate backend services, no Mongo/ES/SNS/gRPC/SES).

"DIGITAL_SIPPOY" is a project-name segment folded into the branch name per
the user's instruction ("same repo, just add it in the name of the
branches"), ahead of the LANG_V{version} segment.

Inputs (not part of this repo, same reasoning as generate_branches.py):
  TEMPLATE_DIR   a clean copy of the Next.js app (app/, lib/, public/,
                 package.json, next.config.ts, tsconfig.json, Dockerfile,
                 docker-compose.yml, .gitignore — no node_modules/.next/
                 lockfiles)
  LOCKFILE_SETS  <pm>/<lockfile files> for pm in npm|yarn|pnpm|bun, each
                 verified with a real `next build` under Node 20 from a
                 frozen/immutable install before being folded in here.

Usage: python3 _generator/generate_sippoy_branches.py
Run from the repo root, on a clean working tree (checks out its own
branches, so any uncommitted changes on the current branch are lost).
"""
import os
import shutil
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKFILE_SETS = os.environ.get("LOCKFILE_SETS", "/tmp/sippoy-lockfile-sets")
TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", "/tmp/sippoy-template")

BUNDLERS = {
    "ESBUILD": {
        "label": "esbuild",
        "detail": "Next.js's own default build tool is used instead (Webpack, the `next build` "
        "default in Next.js 15.5.12). esbuild is not a pluggable bundler for `next build` — "
        "Next.js's build pipeline is not built on esbuild the way Angular's Application "
        "Builder is, so there is no supported way to select it here. This branch documents "
        "the substitution honestly rather than mislabeling Webpack output as esbuild.",
    },
    "VITE": {
        "label": "Vite",
        "detail": "Next.js's own default build tool is used instead (Webpack, the `next build` "
        "default in Next.js 15.5.12). Vite is not a pluggable bundler for `next build` either "
        "— Next.js has its own separate build pipeline unrelated to Vite's. This branch "
        "documents the substitution honestly, the same way the Vite-labeled branches in the "
        "record-platform-stack (JS_V22_*) matrix do for Angular.",
    },
    "ROLLUP": {
        "label": "Rollup",
        "detail": "Next.js's own default build tool is used instead (Webpack, the `next build` "
        "default in Next.js 15.5.12). Rollup is likewise not selectable as the underlying "
        "bundler for `next build`. This branch documents the substitution honestly, matching "
        "how the Rollup-labeled branches in the record-platform-stack (JS_V22_*) matrix "
        "handle the same situation for Angular.",
    },
}

PACKAGE_MANAGERS = {
    "NPM": {"label": "npm", "install": "npm ci", "run": "npm start", "dev": "npm run dev", "build": "npm run build"},
    "YARN": {"label": "yarn (Berry)", "install": "yarn install --immutable", "run": "yarn start", "dev": "yarn dev", "build": "yarn build"},
    "PNPM": {"label": "pnpm", "install": "pnpm install --frozen-lockfile", "run": "pnpm start", "dev": "pnpm dev", "build": "pnpm build"},
    "BUN": {"label": "bun", "install": "bun install --frozen-lockfile", "run": "bun run start", "dev": "bun run dev", "build": "bun run build"},
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


def install_lockfiles(project_dir, pm):
    src_dir = os.path.join(LOCKFILE_SETS, pm.lower())
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
    branch_name = f"DIGITAL_SIPPOY_JS_V20_{bundler_key}_{pm_key}_{arch_key}"

    return f"""# Digital Sippoy — {branch_name}

This branch is one cell of the Digital Sippoy bundler x package-manager x
architecture matrix, living in the same repo as the record-platform-stack
(`JS_V22_*`) matrix. All 24 `DIGITAL_SIPPOY_JS_V20_*` branches ship the exact
same application code — they differ **only** in bundler, package manager,
and this README's architecture-note label.

## This branch's combination

| Axis             | Value |
| ----------------- | ----- |
| Bundler            | {bundler['label']} |
| Package manager    | {pm['label']} |
| Architecture note  | {arch_label} |

> **Bundler substitution note:** {bundler['detail']}

> **Architecture-note caveat:** "{arch_label}" is a label only. Every branch
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

Or locally with {pm['label']} (Node 20 required):

```bash
{pm['install']}
{pm['dev']}      # dev server
{pm['build']}    # production build
{pm['run']}      # after building
```
"""


def main():
    branches = []
    for bundler_key in BUNDLERS:
        for pm_key in PACKAGE_MANAGERS:
            for arch_key in ARCHITECTURES:
                branches.append((bundler_key, pm_key, arch_key))

    print(f"Generating {len(branches)} Digital Sippoy branches...")

    for bundler_key, pm_key, arch_key in branches:
        branch_name = f"DIGITAL_SIPPOY_JS_V20_{bundler_key}_{pm_key}_{arch_key}"
        print(f"--- {branch_name} ---")

        run(["git", "checkout", "--orphan", "tmp-sippoy-branch-build"])
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

        clear_lockfiles(REPO_ROOT)
        install_lockfiles(REPO_ROOT, pm_key)

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
        run(["git", "branch", "-m", "tmp-sippoy-branch-build", branch_name])

    print("All Digital Sippoy branches generated.")


if __name__ == "__main__":
    main()
