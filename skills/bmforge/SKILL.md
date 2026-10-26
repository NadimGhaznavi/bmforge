---
name: bmforge
description: Set up a new Git repository with locally pinned BMForge engineering skills. Present available components, gather the user's choices, and bootstrap the project; do not generate application features.
---

# BMForge for Codex

This is BMForge's **single user-level skill**, invoked with `$bmforge` in Codex and installed at `~/.agents/skills/bmforge/`. The other BMForge skills are **not** global prerequisites. Discover them from this catalogue and install only those selected into the new project's `.agents/skills/`.

## Available skills

Always installed:
- `bmforge-project`: engineering contract, application architecture and changelog discipline.
- `bmforge-constants`: typed, domain-grouped identifiers.
- `bmforge-localization`: English message keys and optional runtime translations.
- `bmforge-installation`: application-owned install, upgrade and uninstall lifecycle.

Optional, selected by requirement:
- `bmforge-http`: standard-library HTTP server and optional Jinja2 display.
- `bmforge-zmq`: PyZMQ REQ/REP server.
- `bmforge-db-server`: canonical MariaDB manager and domain data-access interfaces.
- `bmforge-git`: Git commit and managed-file publishing.
- `bmforge-visualization`: Plotly.js charts, Leaflet maps and Cytoscape.js graphs.
- `bmforge-gif-animation`: Pillow GIF generation from rendered frames.
- `bmforge-rca`: read-only production evidence collection and local root-cause analysis.

Explain relevant capabilities and ask the user which optional skills to install. **Never select all by default** or silently add infrastructure. A baseline-only installation is valid.

## Set up a new project

1. Work at the root of a **new Git repository**. Ask before initializing Git if necessary. Do not overwrite an existing `AGENTS.md` or `.agents/`. Do not attempt to adopt an established application.
2. Ask for the canonical Python application class name (such as `SnakeLab`) and optional CMDB subtype (default `Application`). Never infer the Python name from a repository slug.
3. With the user's selection, invoke this skill's installer, for example:

   ```sh
   python3 ~/.agents/skills/bmforge/scripts/manage.py init \
       --project /path/to/new-repository --name AcmeApp \
       --components bmforge-http,bmforge-db-server
   ```

   Omit `--components` for a baseline-only project. Prefer `--source "$HOME/.cache/bmforge-upstream"` when that local BMForge checkout exists and is clean; otherwise the first bootstrap can clone BMForge `main` once. No app code, services, databases or deployments are generated.
4. Verify the resulting `AGENTS.md`, pinned skills, `.agents/bmforge/lock.json`, local manager and release scaffold. Report the installed skills and pinned revision. The scaffold prepares, but **does not run**, release or deployment operations.
5. Commit or push nothing without user authorization. After the user reviews and commits the scaffold on local `main`, a separately approved `python3 .agents/bmforge/manage.py setup-branches --project . --dry-run` may be followed by `setup-branches` to create local `dev` and a feature branch. No remote refs or releases are created automatically.

## Subsequent work

- When the user requests another component for a BMForge-bootstrapped project, explain it and use `python3 .agents/bmforge/manage.py add --project . --components <selected-name>`. Refuse to overwrite installed skills. The user need not know manager syntax.
- Before the first BMForge-derived edit in a Codex session, run `python3 .agents/bmforge/manage.py check --project .`. It reads the separately maintained clean `~/.cache/bmforge-upstream` checkout, reports pinned-skill integrity and available changes, and **never** fetches or upgrades. Refresh the upstream checkout separately only when authorized. A missing or stale cache does not invalidate installed skills.
- An available update is a notification, not permission to replace local files. There is no automatic upgrade command. Never change approved dependencies or apply new contracts without explicit approval.

Only project-local skills own an application's engineering requirements and reference code. Each application implements and tests its own code; BMForge is never imported as a runtime dependency.
