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

## 2026-10-26: one Codex entry-point skill

**User experience.** The global `bmforge` skill is the single public entry point for a new repository. It describes the available `bmforge-*` skills and lets Codex install the selected, pinned project-local bundles. Users invoke `$bmforge` instead of managing component installers themselves. Manager commands, branch operations and update-cache details remain agent-facing; public documentation covers only installation, invocation and the resulting guarantees. No legacy `bmforge-new-project` alias or existing-application adoption workflow is maintained.

## 2026-10-26: explicit implementation authorization

**Human control.** Codex may investigate read-only, discuss possibilities and
propose specifications before implementation is authorized. None of those
activities implicitly grants permission to change files. A clear user directive
to implement an agreed scope opens the gate without a prescribed phrase; the
agent then executes the approved work without repetitive per-file approval.
New dependencies and material scope or architecture changes require another
decision. Permission to implement does not imply permission to commit, push,
release or deploy.

**Propagation.** The gate belongs in BMForge's engineering contract and
agent instructions, the single entry-point and baseline project skills, and
the generated project `AGENTS.md`. Existing projects retain pinned guidance
until deliberately updated; read-only update checks report new policy.

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

## 2026-10-24: GIF animation component

**Boundary.** Generate animated GIFs from application-rendered image frames using a separate optional `bmforge.gif-animation` component. The consuming application renders frames and owns camera capture, timing policy, storage and publication. BMForge provides a copyable Python `GIFAnimation` interface template, not a cross-application GIF service.

**Technology and provenance.** Pillow 12.3.0 (`PIL.Image`), `io` and `pathlib` are the approved encoder dependencies. Preserve indexed image palettes where supplied; use cumulative GIF centisecond timing to avoid drift; support byte and file output. The Snake Web `SimulationAnimation` is frozen as an actual source reference, with no Snake-specific code in the template. The skill is optional and pinned; the specification is draft 0.1.0. See `pages/component-gif-animation.md`.

## 2026-10-24: installable Codex component skills

**Greenfield workflow.** A global `bmforge` skill uses a deterministic Python/Git bootstrap tool to install `bmforge-project` and only explicitly selected component skills in a new repository's `.agents/skills/`. The generated `AGENTS.md` supplies start-of-session architecture and update-check instructions. The chosen component's contract and references are **copied locally at a pinned source SHA**; BMForge remains neither a runtime dependency nor a shared framework. No application, service or database is generated by installing skills. Use an application such as DevLog only as a conceptual example, not as an implicit target.

**Updates.** The project carries an independent manager and lock of per-skill content fingerprints and source commits. A read-only `check` compares installed skill content against a separately refreshed local BMForge `main` checkout and notifies Codex of relevant changes, local modifications or unavailable checks. It **never silently upgrades**. The bootstrap tool has no implicit upgrade command; upgrades require user approval and separate review. Adding *new* skills is an explicit command that will not overwrite existing ones. See `pages/codex-skills.md`.

## 2026-10-24: constants and runtime localization from greenfield

**Constants.** Specify domain-grouped `<app>/constants/D<Name>.py` classes with stdlib `typing.Final`, `enum.StrEnum` and `enum.IntEnum`, using Snake Lab and BMGeoIP as frozen examples. Do not introduce an elaborate constants metaclass or treat incidental literals as magic; machine-facing identifiers remain stable regardless of display language. The `bmforge-constants` contract is draft `0.1.0`.

**Runtime localization.** Every new application prepares stable `DText` message keys, an English UTF-8 JSON catalogue and a standard-library, request-scoped `Localizer` from the beginning. Manual choice takes precedence over language preferences, language fallback uses explicit parent tags only, and missing translated messages fall back to English. No automatic translation, Jekyll dependencies, extra Python packages or invented second-language catalogues. The minimal-mistakes fork and blog are pinned as design references, but their *static Jekyll documentation* translation process remains separate. The `bmforge.localization` contract is draft `0.1.0`.

**Bootstrap.** `bmforge-project`, `bmforge-constants`, and `bmforge-localization` are the three greenfield baseline skills; optional HTTP, ZMQ, DB, Git and visualization components remain explicitly selected. Existing installed projects retain their pinned skills. The update checker continues to notify only and never auto-upgrades.

## 2026-10-24: release scaffolding during greenfield bootstrap

**Reuse the original wheel.** The bootstrap now adapts `templates/project/scripts/new-release.sh` with the user's explicit canonical Python application name, preserving its tested feature → dev → main workflow, annotated tags and atomic release push. This is the same mature process running in Snake Lab, BMGeoIP, CMDB, MyCount and other applications. Repository slugs are not reliable application names, so the name is required.

**Prerequisites, not release execution.** Bootstrap copies the existing changelog, CMDB checker, literal version metadata, and the executable lifecycle scripts plus the disabled install.py template. It makes no branch changes, commits, pushes, tags, deployments or release invocations. Pre-existing files and symlink destinations are never overwritten.

**Pinned and notification-only.** Original release templates and guides are included inside `bmforge-project` so project-local update checks report template changes. Generated files are application-owned and are never automatically replaced. Already initialized projects retain their pinned content until an approved, reviewed upgrade.

## 2026-10-24: use DevLog to close installation lifecycle gaps

**Observed evidence.** The first BMForge skill consumer, DevLog, reuses the canonical DbMgr and Localizer unchanged and follows the approved UI/ZeroMQ/DAL contracts. Its deployment required extra application-specific work: a client-only `install.sh -server HOST`, a separate `install-server.sh`, a saved `conf/installation.json` role, and role-preserving upgrades. The pinned GitHub revision has **no `uninstall.sh`**. This demonstrates a missing *installation completion requirement*, not a reason to transplant DevLog's deployment helper as a mandatory library.

**Fourth greenfield baseline.** Install `bmforge-installation` alongside project, constants and localization. The new contract requires all three lifecycle operations to be implemented and tested after actual application requirements are known. Bootstrap still creates **inert** installer scripts, never touches an installed host, and never triggers release publication.

**Minimal and split roles.** Every successful installation, including a client or custom library, owns `D<Name>.BASE_DIR` and records a last-successful `.deployment-version`, a readable CMDB constants file and a managed-file ownership record. Adapt the existing BMForge `install.py` for source-only or metadata-minimal distribution. Optional separate `install-server.sh` and client/server role-aware deployment are only for applications whose requirements demand them. Client upgrades never silently acquire server dependencies or services; uninstall must be implemented for every supported role. Pin DevLog source as reference evidence, not a runtime dependency, and do not change DevLog.

**Version and failure integrity.** Where a package also declares a `pyproject.toml` version, validate that it matches `D<Name>.VERSION`; only advance installed-version markers after verification. A release preflight that merely checks scripts are executable does not certify deployment readiness. Keep BMForge's read-only skill update mechanism and original release workflow unchanged.

## 2026-10-24: package metadata follows the canonical release version

**Root cause from DevLog.** BMForge's release script updated the application constant but did not synchronize a package's PEP 621 `[project].version`. This created a potential disagreement between installed package metadata and CMDB's version. Preserve the release script's existing Git workflow; add an optional literal-version preflight check and update `pyproject.toml` in the same release commit as constants/changelog. Reject mismatched, duplicated or dynamic `[project].version` instead of silently shipping divergence. Projects with tool-only `pyproject.toml` files remain supported. Regression tests use disposable Git remotes. This decision belongs to **BMForge**, while application-specific deployment and release notes remain owned by DevLog.

**Role-aware inventory observation.** DevLog also demonstrated that a client-only installation cannot advertise local server databases or listeners simply because the canonical source constants describe the complete application. Require installed CMDB declarations to reflect the installed role, without changing source identifiers or software version. This is a contract clarification, not a shared runtime dependency.

## 2026-10-24: contract-directed invalid input, preflight and release branches

**ZeroMQ boundary.** DevLog's independent audit demonstrated that syntactically valid JSON with a lone escaped Unicode surrogate can reach application code, fail UTF-8 encoding, and be treated as a fatal worker error. Extend the ZMQ draft specification to `0.3.1`: the transport must reject all invalid Unicode scalar values, including nested values and object keys, with `invalid_request` and continue serving. A subsequent valid request on the same listener is mandatory acceptance evidence. Application handler failures remain visibly fatal.

**Role-aware installation preflight.** A fresh DevLog server installation omitted the required `mariadb` executable from its preflight, allowing a false-positive `--check` and failure after side effects. Revise the installation draft specification to `0.1.1`: preflight must validate every executable required by the selected role **and operation**, before host changes, including the dry-run path. Client-only installation and non-provisioning upgrades must not require server DB administration commands.

**Safe local Git branch bootstrap.** The Git release contract prescribes `main → dev → feat/maint-...`, but the new-project skill originally left all branch setup manual. Add a project-local `setup-branches` action to `manage.py`, explicitly offered **after a reviewed first commit on local `main`**. Provide a read-only `--dry-run` and refuse uncommitted/unborn or existing/remote-tracked refs. The action creates local `dev` and the approved feature branch, **without committing, tagging, pushing or modifying the remote**. No automatic branch setup occurs during initial file generation.

**Application implementation:** Fix the two DevLog defects in DevLog's own repository with its own tests and changelog. Preserve project-local pinned skills and the BMForge update-notification policy; do not silently upgrade consuming applications.

## 2026-10-25: offline BMForge skill update comparison

**Problem.** A fresh GitHub clone on every Codex session creates an unnecessary network dependency. Some Codex execution environments cannot reach GitHub even while the installed skills are fully usable.

**Separation.** Use a single dedicated clean BMForge checkout on `main` as a locally cached source snapshot. Refresh its Git history independently of Codex sessions. The project-local `manage.py check` remains read-only and now compares only against a local checkout, defaulting to `~/.cache/bmforge-upstream`; an explicit `BMFORGE_SOURCE` or `--source` can select another clean checkout. A stale cache cannot certify the latest GitHub state, so the check reports the local source revision.

**Integrity.** Dirty and non-`main` source checkouts are rejected to avoid treating in-progress development as published standards. Installed skill content is still checked against its pinned fingerprint separately: `LOCALLY MODIFIED` is not cleared by a source refresh. Existing project-local managers remain pinned until an owner-approved upgrade.

## 2026-10-25: changelog completeness and timely summaries

**Decision.** Updating `CHANGELOG.md` is part of completing every logical change, including small code, test, documentation, configuration, and maintenance changes. Entries belong in the current `Unreleased` section during the same work item, not in a later release-preparation pass. Related edits may be consolidated; separate completed changes should not disappear from the record.

**Narrative.** Create or refresh a single `### Summary` routinely for meaningful features, bug fixes, reliability or workflow improvements, even if only one change is involved. Keep the summary accurate as additional work accrues. A purely trivial edit need not have a redundant summary.

**Distribution.** The policy lives in the engineering contract, the maintenance guide, BMForge's own agent instructions, the pinned project skill, and generated project `AGENTS.md`. Bundle the maintenance guide for offline use and report its revisions through existing approval-only pinned-skill checks. No new release automation or retroactive rewriting of released history is required.

## 2026-10-25: dark GUI design standard for the HTTP component

**Purpose.** New HTTP applications with human-facing HTML should start with a coherent dark interface inspired by BMDynIP's practical operational layout and readable panels, forms and tables. This is presentation guidance, not transport technology or a mandate for API-only projects to create a GUI.

**Color choice.** Let the implementing AI select each application's dark palette. Prefer saturated primary hues and strong contrast, **avoid pastels**, and provide accessible status, focus, and responsive behavior. Do not require BMDynIP's exact colors or copy its business functionality.

**Reference and traceability.** Pin the BMDynIP HTML/CSS snapshots at `2077300e7ee20de5328164115a277f353ed19579` into the project-local HTTP skill and advance `bmforge.http-server` to `0.4.0`. The rule applies to new implementations; no existing application is modified or migrated.

## Work not yet implemented

- Package any future BMForge components as additional Codex skills only when required; existing global/bootstrap and component skills are implemented but still require real Codex-session validation.
- Implement CMDB-side polling of application health endpoints and simple red/green reporting; BMForge defines the application contract only.
- Add optional static CMDB component discovery and comparison reporting. Do not conflate architectural component metadata with `CMDB_COMPONENTS` filesystem backup declarations.
- Continue using real application implementations to validate component and lifecycle contracts, and publish immutable specification revisions after validation.

## Changing a decision

When a new requirement changes an engineering principle or architectural boundary, update the relevant contract and amend this record with the reason. Keep historical decisions visible rather than silently rewriting their rationale.
