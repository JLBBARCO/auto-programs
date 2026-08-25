# Programs Manager — Repository Specs

This `.specs/` folder documents the `JLBBARCO/programs-manager` repository, split by
sub-project. It's a reference for anyone (human or AI) picking up the codebase without
prior context.

## Repository layout

| Path | Project | Language/Stack |
|---|---|---|
| `core-app/` | **Programs Manager** — the main desktop app | Python 3.12, CustomTkinter |
| `user-generator/` | **Programs Manager User Generator** — companion CLI/GUI tool | Python 3.12 |
| `website/` | **Programs Manager Website** — live log viewer | TypeScript, React, Vite, Express |
| `src/` | Shared assets and Windows-shortcut helpers used by both Python apps | Python |
| `.github/` | CI/CD workflows and release automation scripts | GitHub Actions |

Root-level files:

- `requirements.txt` — shared Python dependencies for `core-app` and `user-generator`
  (PyInstaller, CustomTkinter, pandas, pytest, ruff, etc).
- `version.txt` — a `system_version=YYYY.MM.DD.HHMMSS` marker. This file is regenerated
  by CI at build time from the commit timestamp; the copy in the repo root is not the
  source of truth.
- `code-signing-cert.cer` / `.pfx` / `.pfx.base64.txt` — a self-signed Authenticode
  certificate used to sign the Windows executables. The public `.cer` is what end users
  import to trust the signed binaries.
- `LICENSE`, `CNAME` (GitHub Pages custom domain, legacy).

Per-project details live in:

- [`core-app/OVERVIEW.md`](core-app/OVERVIEW.md)
- [`user-generator/OVERVIEW.md`](user-generator/OVERVIEW.md)
- [`website/OVERVIEW.md`](website/OVERVIEW.md)

## CI/CD pipeline (`.github/`)

Three workflows build and publish native executables for both Python apps, triggered by
path-filtered pushes/PRs to `main` and `develop`, plus manual `workflow_dispatch`:

- **`build-core-app.yml`** — builds `core-app` for Windows and Linux via
  `core-app/build.bat` / `core-app/build.sh` (PyInstaller under the hood).
- **`build-user-generator.yml`** — same pattern for `user-generator`.
- **`release.yml`** — triggered by `workflow_run` after either build workflow succeeds
  (or manually). Downloads the build artifacts, publishes/updates a GitHub Release, and
  uploads the packaged assets.
- **`screenshots.yml`** — regenerates app screenshots (see `core-app/scripts/`).

### Versioning

Versioning is **commit-timestamp-based**, not a file tracked across commits:

1. During each build job, CI reads the checked-out commit's own timestamp
   (`git show -s --format=%cI HEAD`, not the runner's wall clock) and writes
   `system_version=YYYY.MM.DD.HHMMSS` (UTC) into `version.txt`.
2. This guarantees the Windows and Linux legs of the same commit produce an identical
   version string, and that re-running a build for the same commit is reproducible.
3. `version.txt` is copied into the packaged build output (`dist/.../version.txt`) so
   the launcher scripts (`run.ps1` / `run.sh`) and the release workflow can read it back
   out of the artifact — there's nothing to keep in sync or that can merge-conflict
   across branches.
4. `release.yml` extracts `version.txt` from the built archive to compute the release
   tag (`vYYYY.MM.DD.HHMMSS`), with a `-rN` suffix appended only in the unlikely case two
   builds land in the same second.

This design replaced an earlier approach (`bump_version.py` incrementing a semver file
tracked in git), which suffered from non-fast-forward push races between concurrent
workflow runs and merge conflicts on the version file. `.github/scripts/bump_version.py`
is kept for reference/manual use but is no longer part of the automated pipeline.

### Branch behavior

- `main` → stable release (`--latest`, title "Latest release").
- `develop` → prerelease (`--prerelease`, title "Pre-release").
- Any other branch is rejected by `release.yml`.

### Code signing

Windows executables are optionally signed with a self-signed Authenticode certificate:

- The `.pfx` is stored base64-encoded in the `CODE_SIGN_PFX_BASE64` GitHub secret,
  decoded on the runner, imported into the local trust store (runner-only, so
  `signtool verify` doesn't flag the self-signed root), used to sign via `signtool sign`,
  then removed.
- `CODE_SIGN_TIMESTAMP_URL` defaults to DigiCert's timestamp server.
- End users must import the public `code-signing-cert.cer` themselves to fully trust the
  binary; this is documented in the relevant README.
- `.github/scripts/generate-self-signed-cert.ps1` generates the certificate pair.

### Auto-updating launchers

`core-app/run.ps1` / `run.sh` and `user-generator/run.ps1` / `run.sh` are meant to be
piped directly from GitHub raw (`irm ... | iex` / `curl ... | bash`). They:

1. Prefer a local build (`dist/` or `build/` next to the script) if present.
2. Otherwise install to `~/.programs-manager` (Unix) — downloading the latest release
   asset matching the current OS.
3. On subsequent runs, compare the installed `version.txt` against the latest GitHub
   release/prerelease (selected via `AIP_BRANCH`/`SCRIPT_BRANCH=develop` to opt into
   prereleases) and re-download only when a newer version is available.
4. Create a desktop shortcut/`.desktop` entry (Linux) or `.command` file (macOS) pointing
   at the resolved executable.

A known unresolved issue (as of last contact): on Windows, application-control policies
(e.g. WDAC/AppLocker-style restrictions) can block the `Programs Manager.exe` launcher
script from running.
