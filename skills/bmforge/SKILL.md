---
name: bmforge
description: Bootstrap new applications or attach selected, pinned engineering skills to an existing repository without changing its architecture or release workflow.
---

# BMForge for Codex

This is BMForge's **single user-level skill**, invoked with `$bmforge` in Codex and installed at `~/.agents/skills/bmforge/`. The other BMForge skills are **not** global prerequisites. Discover them from this catalogue and install only those selected into the project's `.agents/skills/`. Use `init` for a new application or `attach` for an established one.

## Available skills

Always installed **for new-project bootstrap only**:
- `bmforge-project`: engineering contract, application architecture and changelog discipline.
- `bmforge-constants`: typed, domain-grouped identifiers.
- `bmforge-localization`: English message keys and optional runtime translations.
- `bmforge-installation`: application-owned install, upgrade and uninstall lifecycle.

Optional, selected by requirement:
- `bmforge-http`: standard-library HTTP server and optional Jinja2 display.
- `bmforge-timeline`: vis-timeline editing of dated objects and ranges; requires `bmforge-http`.
- `bmforge-zmq`: PyZMQ REQ/REP clients and servers over TCP or named local IPC sockets.
- `bmforge-nftables`: host-local timed IP bans, removal and inspection in one owned table.
- `bmforge-security-events`: independent fire-and-forget security-event producer using journald and trusted request-scoped source binding; no HTTP, ZMQ, Fail2ban or nftables prerequisite.
- `bmforge-fail2ban`: native **journald** security-event filters/jails and a thin local ban action client; requires `bmforge-zmq` in the blocking project only.
- `bmforge-db-server`: canonical MariaDB manager and domain data-access interfaces.
- `bmforge-git`: Git commit and managed-file publishing.
- `bmforge-github-pages`: project documentation sites with the shared dark theme, required logo, canonical configuration and publishing scaffold; no HTTP or Git component prerequisite.
- `bmforge-visualization`: Plotly.js charts, Leaflet maps and Cytoscape.js graphs.
- `bmforge-gif-animation`: Pillow GIF generation from rendered frames.
- `bmforge-rca`: read-only production evidence collection and local root-cause analysis.

Explain relevant capabilities and ask the user which optional skills to install. **Never select all by default** or silently add infrastructure. A baseline-only installation is valid.

For timeline editing, explicitly select `bmforge-http,bmforge-timeline` together, or add timeline when HTTP is already pinned in the project. The manager rejects a missing HTTP dependency before writing files and never installs it implicitly.

For an application that only produces security events, select **`bmforge-security-events` alone**. Its application business logic calls `emit("abuse")` and knows no IP, ban policy, Fail2ban/ZMQ or retry mechanics. The application's trusted ingress adapter supplies the source, and its existing systemd unit sends the event through **journald**.

For a blocking service, select `bmforge-zmq,bmforge-fail2ban,bmforge-nftables` as needed. Fail2ban requires ZMQ only in this consumer project; nftables is independently selectable. Native Fail2ban reads producing-service journal events, counts them within its configured window and invokes the existing ban action. Do not require any of these enforcement skills in an event-producing application. These skills cover only this small integration subset.

## Implementation authorization gate

Discussion, component exploration and approval of a design do not themselves
authorize edits. Inspect and explain read-only until the user clearly asks
you to proceed with the agreed setup or implementation. No fixed phrase is
required. Once authorized, complete that scope without repeated prompts,
but pause for new dependencies or material scope or architecture changes.
Implementation permission does not authorize commits, pushes or deployments.

## Set up a new project

1. Work at the root of a **new Git repository**. Ask before initializing Git if necessary. Do not overwrite an existing `AGENTS.md` or `.agents/`. Do not attempt to adopt an established application.
2. Ask for the canonical Python application class name (such as `SnakeLab`) and optional CMDB subtype (default `Application`). Never infer the Python name from a repository slug.
3. Explain the files and pinned skills the installer will create, and get an **explicit go-ahead** before invoking it. A direct instruction to perform the described setup is sufficient. For example:

   ```sh
   python3 ~/.agents/skills/bmforge/scripts/manage.py init \
       --project /path/to/new-repository --name AcmeApp \
       --components bmforge-http,bmforge-db-server
   ```

   Omit `--components` for a baseline-only project. Prefer `--source "$HOME/.cache/bmforge-upstream"` when that local BMForge checkout exists and is clean; otherwise the first bootstrap can clone BMForge `main` once. No app code, services, databases or deployments are generated.
4. Verify the resulting `AGENTS.md`, pinned skills, `.agents/bmforge/lock.json`, local manager and release scaffold. Report the installed skills and pinned revision. The scaffold prepares, but **does not run**, release or deployment operations.
5. Commit or push nothing without user authorization. After the user reviews and commits the scaffold on local `main`, a separately approved `python3 .agents/bmforge/manage.py setup-branches --project . --dry-run` may be followed by `setup-branches` to create local `dev` and a feature branch. No remote refs or releases are created automatically.

## Attach skills to an existing project

Existing applications keep their own architecture, coding guidelines, dependencies, branches, changelog and release process. Do not run `init`, overwrite `AGENTS.md` or replace an existing `.agents/` tree. **Do not install the greenfield baseline automatically.** Ask which optional skills the user actually needs; `bmforge-rca` may be installed alone.

1. Inspect the repository read-only to establish its existing project instructions and selected skill paths. Explain what will be added and get explicit authorization before attaching anything.
2. After approval, from the repository root run:

   ```sh
   python3 ~/.agents/skills/bmforge/scripts/manage.py attach \
       --project . --components bmforge-rca
   ```

   Substitute the chosen optional components. Prefer `--source "$HOME/.cache/bmforge-upstream"` when a suitable local checkout exists, otherwise the first attachment may clone BMForge `main`. The command copies only the requested pinned skills and the BMForge manager and lock file; it preserves existing `AGENTS.md`, other skills, source, configuration, release scripts and Git refs.
3. Confirm `.agents/bmforge/lock.json`, `.agents/bmforge/manage.py` and the selected `.agents/skills/` directories. Use the installed skill in Codex by its name, such as `$bmforge-rca`. Follow the application's existing instructions for everything outside the selected skill's scope.
4. Subsequent `add` and read-only `check` work for attached projects. `setup-branches` is **new-project-only**; never run it on an established repository. Attachment never authorizes remote access, production changes, application edits, commits, pushes or deployments.

## Subsequent work

- When the user requests another component for a BMForge-managed project (new or attached), explain it and obtain explicit permission to add it before using `python3 .agents/bmforge/manage.py add --project . --components <selected-name>`. Refuse to overwrite installed skills. The user need not know manager syntax.
- Before the first BMForge-derived edit in a Codex session, run `python3 .agents/bmforge/manage.py check --project .`. It reads the separately maintained clean `~/.cache/bmforge-upstream` checkout, reports pinned-skill integrity and available changes, and **never** fetches or upgrades. Refresh the upstream checkout separately only when authorized. A missing or stale cache does not invalidate installed skills.
- An available update is a notification, not permission to replace local files. There is no automatic upgrade command. Never change approved dependencies or apply new contracts without explicit approval.

Only project-local skills own an application's engineering requirements and reference code. Each application implements and tests its own code; BMForge is never imported as a runtime dependency.
