---
title: BMForge Design Decisions
lang: en
locale: en-US
language_name: English
translation_key: bmforge-decisions
permalink: /decisions/
---

# BMForge decision record

This file preserves design decisions that should not disappear into conversations. It is a record, not a replacement for the authoritative contracts linked below.

## 2026-10-24: agent-first BMForge

**Purpose.** BMForge teaches Codex the desired software-development process and construction patterns. It is not a shared library or an orchestration platform. Every destination application owns its generated or adapted code. Cross-project integrations use documented public APIs only.

**Construction.** Component specifications define required behaviour and acceptance tests; pinned example code lives inside BMForge. Skills will eventually package the instructions for Codex. The contracts remain authoritative so independent copies do not drift.

**Engineering priorities.** Lean implementations, contract trust, explicit distributed-operation results, and visible fail-fast errors outrank speculative resiliency. Validate at untrusted boundaries. No unrequested feature layers. See `pages/engineering-contract.md`.

**Traceability.** Component-owning modules declare a literal `BMFORGE_COMPONENT` with stable ID and specification version. Published specification versions must remain retrievable. A future CMDB source scanner can report application/spec relationships and outdated versions; a version marker does not prove compliance. See `pages/specification-lifecycle.md`.

**Current scope.** HTTP and ZeroMQ remain draft `0.3.0`; DB Server is draft `0.4.0` with a canonical application-independent `DbMgr.py`, and Git is separately versioned. The implementations and pinned examples will be validated by consuming applications. DevLog will test whether the contracts are sufficient.

## 2026-10-24: minimal application health checks

**Monitoring.** Running applications answer on-demand health checks through their existing HTTP or ZeroMQ interface. HTTP `GET /health` returns `200` (green) or `503` (red) and identifies required component failures. The DB Server check runs inside the application on its configured connection; CMDB never logs into MariaDB for this check. No dedicated health service, background polling, retry engine, or self-recovery architecture. See `pages/health-checks.md`.

## 2026-10-24: explicit approved runtime modules

**Technology decisions.** Every component's specification defines the complete approved Python module inventory for its reusable infrastructure, with roles and local frozen examples. A consuming application's business activities are not covered by a component's module list. Codex must not add a new infrastructure package, switch to Django or another server, replace PyZMQ/PyMySQL, or change architecture merely to satisfy a task. If a required capability is missing, stop and obtain user approval, then change the specification or add another component before coding. Plotting, mapping and network visualization now have a dedicated optional component; GeoIP-client and logging patterns remain separate candidates, not hidden dependencies of HTTP/ZeroMQ/DB Server. The original three draft contracts are advanced to `0.3.0`.

## 2026-10-24: Git component

**Scope.** A separate Git component supports exactly two operations: `Publish` (approved generated files in a dedicated checkout, based on the frozen Snake Web `GitPublisher`) and `Commit` (`git add . -v`, `git commit -m <message>`, `git push` from the caller's repository root). Its standalone template and integration tests are versioned in BMForge. The implementation uses Python standard-library modules plus the Git CLI, not GitPython. Publishing checks and retries are deliberate features of the proven publisher; ordinary commit has no hidden fetch, merge or recovery behaviour. No Git server or monitor endpoint is required. Spec: `pages/component-git.md` (draft 0.1.0).

## 2026-10-24: USDP-inspired class classification and canonical MariaDB DAL

**Responsibility model.** New application code classifies substantial classes as **Activity** (business processing and orchestration), **Interface** (technology bridges and domain-level data access), or **Entity** (data values). These are the project's terms inspired by the Unified Software Development Process's responsibility separation, not framework base classes. Composition and clear source packages carry the classification; no class registry or metadata framework. See `pages/classification.md`.

**MariaDB data access.** Each new database-backed app copies the exact canonical `components/templates/db-server/interface/DbMgr.py` into `<app>/interface/DbMgr.py`, unchanged. Project-specific configuration is supplied by the application. One or more domain interfaces (`VisitorDb`, `MiningDb`, `GeoIpDb`) own the SQL and use the shared manager by constructor composition. Activities call the domain interfaces; entities remain inert data. App-specific interfaces never acquire their own driver connections or bypass `DbMgr`. This is a revised draft DB Server contract `0.4.0`, not an instruction to retrofit all deployed apps immediately.

**Provenance.** The original BMGeoIP reference remains a historical example, and MyCount `VisitDb`, `CollectVisit` and `Visit` are pinned locally to show the three roles. A future CMDB scanner can use the existing `BMFORGE_COMPONENT` marker for component-spec tracing; source classification does not require a new runtime marker.

## 2026-10-24: approved display visualization libraries

**Purpose.** Define the exact approved browser libraries for the visual capabilities already used across MyCount and CMDB: **Plotly.js 4.1.1** for plots, charts and time-series; **Leaflet 1.9.4** for geographic maps; and **Cytoscape.js 3.34.3** for interactive network and relationship graphs. The libraries are selected by need, not automatically attached to every HTTP server. Python's `plotly` package is not required because MyCount renders Plotly in the browser. Jinja2 remains a separate, optional HTTP rendering technology; CMDB uses basic placeholder substitution. See `pages/component-visualization.md` (draft specification 0.1.0).

**Provenance and delivery.** The original MyCount templates and CMDB graph code are pinned inside BMForge at source commits `90574cd838ba43499a825c6a193b43cbc485c91c` and `43438d9c41949ef70a635884a9bd6885d5c5f22c`. Plotly.js and Leaflet are loaded through version-specific CDN URLs in MyCount; CMDB vendors Cytoscape.js and its licence locally, with exact assets copied into BMForge. These are source references and approved dependencies, not runtime cross-project imports.

**Scope.** Codex must obtain owner approval to substitute or upgrade a visualization library, to add a frontend build/framework, or to introduce an alternative plotting backend. Browser visualization has no separate server, HTTP listener or health endpoint. Future CMDB asset/version scanning is separate work and is not added here.

## 2026-10-24: installable Codex component skills

**Greenfield workflow.** A global `bmforge-new-project` skill uses a deterministic Python/Git bootstrap tool to install `bmforge-project` and only explicitly selected component skills in a new repository's `.agents/skills/`. The generated `AGENTS.md` supplies start-of-session architecture and update-check instructions. The chosen component's contract and references are **copied locally at a pinned source SHA**; BMForge remains neither a runtime dependency nor a shared framework. No application, service or database is generated by installing skills. Use an application such as DevLog only as a conceptual example, not as an implicit target.

**Updates.** The project carries an independent manager and lock of per-skill content fingerprints and source commits. A read-only `check` compares installed skill content against fresh BMForge main and notifies Codex of relevant changes, local modifications or unavailable checks. It **never silently upgrades**. The bootstrap tool has no implicit upgrade command; upgrades require user approval and separate review. Adding *new* skills is an explicit command that will not overwrite existing ones. See `pages/codex-skills.md`.

## 2026-10-24: constants and runtime localization from greenfield

**Constants.** Specify domain-grouped `<app>/constants/D<Name>.py` classes with stdlib `typing.Final`, `enum.StrEnum` and `enum.IntEnum`, using Snake Lab and BMGeoIP as frozen examples. Do not introduce an elaborate constants metaclass or treat incidental literals as magic; machine-facing identifiers remain stable regardless of display language. The `bmforge-constants` contract is draft `0.1.0`.

**Runtime localization.** Every new application prepares stable `DText` message keys, an English UTF-8 JSON catalogue and a standard-library, request-scoped `Localizer` from the beginning. Manual choice takes precedence over language preferences, language fallback uses explicit parent tags only, and missing translated messages fall back to English. No automatic translation, Jekyll dependencies, extra Python packages or invented second-language catalogues. The minimal-mistakes fork and blog are pinned as design references, but their *static Jekyll documentation* translation process remains separate. The `bmforge.localization` contract is draft `0.1.0`.

**Bootstrap.** `bmforge-project`, `bmforge-constants`, and `bmforge-localization` are the three greenfield baseline skills; optional HTTP, ZMQ, DB, Git and visualization components remain explicitly selected. Existing installed projects retain their pinned skills. The update checker continues to notify only and never auto-upgrades.

## 2026-10-24: release scaffolding during greenfield bootstrap

**Reuse the original wheel.** The bootstrap now adapts `templates/project/scripts/new-release.sh` with the user's explicit canonical Python application name, preserving its tested feature → dev → main workflow, annotated tags and atomic release push. This is the same mature process running in Snake Lab, BMGeoIP, CMDB, MyCount and other applications. Repository slugs are not reliable application names, so the name is required.

**Prerequisites, not release execution.** Bootstrap copies the existing changelog, CMDB checker, literal version metadata, and the executable lifecycle scripts plus the disabled install.py template. It makes no branch changes, commits, pushes, tags, deployments or release invocations. Pre-existing files and symlink destinations are never overwritten.

**Pinned and notification-only.** Original release templates and guides are included inside `bmforge-project` so project-local update checks report template changes. Generated files are application-owned and are never automatically replaced. Already initialized projects retain their pinned content until an approved, reviewed upgrade.

## Work not yet implemented

- Package any future BMForge components as additional Codex skills only when required; existing global/bootstrap and component skills are implemented but still require real Codex-session validation.
- Implement CMDB-side polling of application health endpoints and simple red/green reporting; BMForge defines the application contract only.
- Add optional static CMDB component discovery and comparison reporting. Do not conflate architectural component metadata with `CMDB_COMPONENTS` filesystem backup declarations.
- Validate the three contracts through DevLog, then publish immutable specification revisions and improve only the gaps the implementation exposes.

## Changing a decision

When a new requirement changes an engineering principle or architectural boundary, update the relevant contract and amend this record with the reason. Keep historical decisions visible rather than silently rewriting their rationale.
