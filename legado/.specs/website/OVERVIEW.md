# website — Programs Manager Website

A TypeScript web app that displays the `log.log` output of a running `core-app`
instance in real time. Deployed on Vercel.

## Stack

- **Client**: React + Vite, Tailwind-style component library under
  `client/src/components/ui/` (Radix UI primitives: accordion, dialog, dropdown, select,
  tabs, tooltip, etc.), `wouter` for routing (patched via `patches/wouter@3.7.1.patch`),
  `framer-motion` for animation, `axios` for HTTP.
- **Server**: Express (`server/index.ts`), bundled with `esbuild` for production.
- **Shared**: `shared/const.ts` — constants shared between client and server.
- Package manager: pnpm (`pnpm-lock.yaml`), though `package-lock.json` is also present.
- Scripts: `dev` (vite --host), `build` (vite build + esbuild bundle of the server),
  `start` (serve the production bundle), `preview`, `check` (`tsc --noEmit`), `format`
  (prettier).

## Frontend behavior

- Language: English (en-US).
- Main view: four containers for `INFO`, `DEBUG`, `WARNING`, `ERROR` log severities.
  Each has a fixed height and horizontal scrollbar; older messages appear above newer
  ones.
- Expected incoming log line format:
  `[dd/mm/yyyy hh:mm:ss] [LEVEL] <message>`
  e.g. `[01/06/2026 12:30:45] [SUCCESS] Visual Studio Code installed` is rendered as
  `01/06/2026 12:30:45 | Visual Studio installed`, with the timestamp colored `#808080`.
- History partitioning: entries older than 1 minute (relative to the page's load
  timestamp) are shown in a separate history section.
- The monitor tracks the latest `Start <program>` and `Operating System: <system>`
  markers so headers/history can be grouped by program run.
- Favicon resolution was recently refactored from server-side to client-side (see
  `client/src/lib/` and the relevant hooks/components for the current implementation).

### Footer — Contact container

Contact cards are loaded from a remote JSON
(`https://raw.githubusercontent.com/JLBBARCO/portfolio/main/src/json/areas/contact.json`,
cached hourly by Vercel) and rendered as circular icon buttons. Hovering shows the
contact `name`; the JSON `url` is the card link; `iconName` selects the icon. Layout:
`display: flex; flex-flow: row wrap; justify-content: space-between; align-items: center;`

### Error page

If the site can't reach the `log.log` port (from the `?port=NNNN` query param, or a
fallback `99xx` port) or the file isn't being shared, an error page is shown with a
refresh button and a link to
`https://github.com/JLBBARCO/programs-manager`.

## Backend behavior (`server/index.ts`)

- Records the page-load time to partition current-run vs. historical logs.
- Tracks the current program name and OS extracted from the log stream.
- Monitoring stops when the latest log line contains `[INFO] End system`.
- **Port probe**: on load, probes `?port=NNNN` if given, else falls back to a sensible
  `99xx` default, retrying for up to 30 seconds. If unavailable, monitoring pauses until
  the user refreshes.

## Key files

| Path | Purpose |
|---|---|
| `client/src/pages/Home.tsx` | Main log-viewer page. |
| `client/src/pages/NotFound.tsx` | 404/error page. |
| `client/src/hooks/useLogMonitor.ts` | Core log-polling/monitoring hook. |
| `client/src/lib/logFetcher.ts` | Fetches log data from the local port. |
| `client/src/lib/logParser.ts` | Parses raw log lines into structured entries. |
| `client/src/contexts/ThemeContext.tsx` | Light/dark theme handling. |
| `client/src/constants/app.ts`, `client/src/const.ts` | App-level constants. |
| `api/` | Vercel serverless function(s). |
| `vite.config.ts`, `vercel.json` | Build/deploy configuration. |

## Deployment

Deployed on Vercel per `vercel.json`. Current domain:
`programs-manager-website-jlbbarco.vercel.app`.
