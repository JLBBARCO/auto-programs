# user-generator — Programs Manager User Generator

Small Python companion app that scans the programs currently installed on the user's
system and generates a `user.json` file in the format `core-app` expects, so the user
doesn't have to hand-author their install/uninstall list.

## Output format

Each detected program becomes one entry:

```json
{
  "name": "Git",
  "type": "install",
  "id": "Git.Git",
  "checkbox": true
}
```

## Main modules (`lib/`)

| Module | Responsibility |
|---|---|
| `system` | OS detection. |
| `list_programs` | Runs package-manager list commands (e.g. `winget`), strips ANSI
  escape codes and terminal noise from the output, and parses installed packages. |
| `find_folders` | Locates relevant folders on disk. |
| `json` | Reads/writes the generated `user.json`. |
| `notifications` | User-facing notifications. |
| `log` | Logging utilities. |

`main.py` (~35 lines) is a thin orchestrator wiring these modules together.

## Build & run

- Source: `python user-generator/main.py` (after `pip install -r requirements.txt`).
- Build: `user-generator/build.bat` (Windows) / `user-generator/build.sh` (Linux) →
  output in `dist/Programs Manager User Generator/`.
- Run/install (auto-updating launcher, piped from GitHub raw):
  - Linux: `curl -fsSL https://raw.githubusercontent.com/JLBBARCO/programs-manager/main/user-generator/run.sh | bash`
  - Windows: `irm https://raw.githubusercontent.com/JLBBARCO/programs-manager/main/user-generator/run.ps1 | iex`
  - The scripts download the latest `latest`-release artifact, extract it to a temp
    folder, and run it.

## CI/CD

`.github/workflows/build-user-generator.yml` runs on pushes to `main`/`develop` that
touch `user-generator/**` (or shared bits like `requirements.txt`, `src/assets/icon/**`),
and can also be triggered manually. It builds:

- Windows via `user-generator/build.bat`
- Linux via `user-generator/build.sh`

then packages the outputs. `.github/workflows/release.yml` publishes/updates the
matching GitHub Release with:

- `programs-manager-user-generator-windows.zip`
- `programs-manager-user-generator-linux.tar.gz`

See the root spec (`.specs/README.md`) for the shared versioning scheme (commit-timestamp
based `version.txt`) and code-signing details, which apply identically here.
