# BMForge agent guidance

BMForge is a **standalone engineering specification repository**, not a runtime library. Every application owns its implementation.

## Codex component skills

The [greenfield skill installer](pages/codex-skills.md) lives under `skills/bmforge-new-project/` and installs self-contained, pinned skills from `skills/bmforge-{project,constants,localization,installation,http,zmq,db-server,git,visualization,gif-animation,rca}/`. Its `manage.py check` is **read-only** and reports changes without applying them. Always install the project/constant/localization/installation baseline and the canonical release-tooling scaffold. Require a canonical `--name` to configure `scripts/new-release.sh` and its existing prerequisites. Never run the release script, commit, tag, push or deploy during file generation. A user-authorized post-commit `manage.py setup-branches` operation may establish the local `dev`/feature branch lineage, but never alters remote branches or pushes automatically. Add other infrastructure only by explicit selection. Keep installer tests hermetic and require user consent for any upgrade.

## Read only what the task needs

1. Read `pages/engineering-contract.md` and `pages/classification.md` first. Build the smallest clear implementation that satisfies the requirement, and fail visibly when internal contracts cannot be met.
2. Follow `pages/component-constants.md` for stable domain-grouped identifiers and `pages/component-localization.md` for runtime UI/CLI messages from the first user-facing feature. These are **different** from `pages/multilingual-documentation.md` (Jekyll documentation).
3. The [Installation Lifecycle](pages/component-installation.md) is mandatory: after implementing an application, complete and test install/upgrade/uninstall, preserve client/server roles if present, and produce a successful-version/CMDB identity under `BASE_DIR`, including library-only installations. DevLog is a reference, not a runtime dependency.
4. Use `index.md` to find the relevant process. For components, read `pages/component-blueprints.md` and only the needed component specifications. For chart, map or graph capabilities, also read `pages/component-visualization.md`. For animated GIF encoding, read `pages/component-gif-animation.md`.
5. Treat each selected component specification's **Approved runtime modules** section as a fixed implementation inventory. Copy/adapt only from that list. If it cannot meet the requirement, **pause and ask the user before adding packages or changing technologies**; don't silently swap in another framework.
6. Use locally pinned reference examples for understanding, not runtime imports. HTTP/ZeroMQ may adapt `components/reference/bmgeoip/`; **DB Server must copy `components/templates/db-server/interface/DbMgr.py` unchanged**, passing app configuration and implementing domain `*Db` interfaces around it. Never fetch moving examples or transplant source-app business logic.
7. Follow existing BMForge configuration, CMDB, install, and release processes when those concerns apply. Never add BMForge or an example project as a runtime dependency. Independent applications interact through documented public APIs.
8. When creating a BMForge-derived component, apply the literal source marker specified in `pages/specification-lifecycle.md`, using the selected specification's ID and version.
9. For a running application, implement the on-demand checks in `pages/health-checks.md` using existing HTTP/ZeroMQ interfaces and the application's own DB layer. Never give CMDB direct MariaDB access.
10. Run the component's acceptance checks in the destination project and report what actually passed, failed, or was not tested. A copied example is not a completed component.

## Changelog discipline

- **Every completed logical change must update `CHANGELOG.md`**, including small code fixes, tests, documentation, configuration, maintenance and refactoring. Record it under the single `## [Unreleased]` heading in the same task, before reporting completion or committing; never defer it until release time. Consolidate related file edits into one clear entry rather than listing individual files.
- **Add or refresh `### Summary` routinely**, even when one meaningful feature, bug fix or operational improvement is the only unreleased change. Explain the outcome and why it matters in plain English. Keep one `### Summary` per unreleased or versioned section, ahead of `Added`/`Changed`/`Fixed` headings. Consult `pages/changelog-maintenance.md` before finishing a task.

## HTTP GUI appearance

For user-facing HTML, follow the HTTP component's `pages/component-http.md` design contract. Treat BMDynIP's pinned HTML/CSS as a **visual reference**: use dark surfaces, strong contrast and AI-chosen saturated primary accents, **not pastel colors**. Keep controls keyboard/mobile accessible. Do not copy its DNS features or create a GUI for an API-only service.

## Engineering rules

- Classify substantial classes explicitly: `activity/` orchestrates work, `interface/` owns external and domain data access, `entity/` carries data. Domain `*Db` classes compose with the unchanged `DbMgr`. Do not put SQL in activity or entity classes.
- Validate untrusted inputs at external boundaries. Trust established internal contracts instead of repeating defensive checks.
- Never introduce a new module, server framework, database driver, ORM, plotting library, or dependency to replace an approved component implementation without explicit user approval and a specification update. Charts use Plotly.js, geographic maps use Leaflet, and relationship graphs use Cytoscape.js at the versions listed in `pages/component-visualization.md`; select only the libraries the application requires.
- Don't swallow exceptions or invent fallbacks, retries, workers, queues, abstractions, or optional features. Include additional complexity only for a named requirement or observed failure.
- A critical distributed operation needs its defined result, timeout, and error semantics. Never claim success before it is known.
- A failed required dependency or unexpected internal state must surface clearly. Gracefully reject invalid external requests without disguising internal defects.
- When improving BMForge, distinguish implementation bugs from contract gaps. Update acceptance checks and specification versions intentionally; record policy-level decisions in `DECISIONS.md`.
- Ask before materially expanding an application's scope. This project is not a licence to build unrequested infrastructure.

For Git publishing or commits, read `pages/component-git.md` and copy `components/templates/git/Git.py` into the application's own namespace. Use only its approved modules. The frozen Snake Web `GitPublisher.py` is a source reference, not a runtime dependency. Do not invent release automation, switch Git libraries, or alter the prescribed commit commands.

For current status and unresolved work, read `DECISIONS.md`. Native component skills are available; CMDB component scanning is planned, not yet present.
