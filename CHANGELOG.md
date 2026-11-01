---
title: Changelog
lang: en
locale: en-US
language_name: English
translation_key: bmforge-changelog
permalink: /CHANGELOG/
---

## [Unreleased]

### Summary

Add native English and Ukrainian SVG architecture diagrams in the established dark
osoyalce visual style, so both BMForge homepages explain the SDLC and its
continuous-improvement loop at a glance.

### Changed

- Replace the English homepage's temporary HTML flow with an accessible SVG.
  Give Ukrainian visitors the same concise overview and a localized SVG.
  Move the former Ukrainian technical catalogue to its own reference page.
- Remove superseded homepage-specific CSS; keep SVGs self-contained, with
  no new Jekyll, runtime or JavaScript dependencies.


## [0.22.0] - 2026-11-01 @ 05:36

### Summary

Keep BMForge's security-event integration standards clean and current: emit
timestamp-free journal messages, match Fail2ban's actual journal-prefixed lines,
and validate the native service end to end. Application updates are explicit
refactors, not compatibility migrations.
The site now separates the brief human-facing SDLC overview from the full
agent-facing engineering reference.

### Changed

- Replace the dense homepage with a responsive SDLC flow and explicit feedback
  loop; retain the existing task index, component catalogue and links in a
  dedicated technical reference without changing runtime specifications.
- Advance Security Events to draft `0.1.1`: omit embedded timestamps from the
  canonical `MESSAGE` and use journald's trusted event time; keep one
  fire-and-forget emit call and no application ban state.
- Advance Fail2ban to draft `0.3.1`: use the native 1.1.x `common.conf` journal
  prefix with unit-scoped matching, separate config/bindings/journal/filter
  checks, and two distinct countable-event acceptance cases with independent
  thresholds and overlapping-jail behavior.
- Define only the current owned native `.conf` defaults and separate operator
  `.local` overrides. Conflicting effective settings fail validation; legacy
  configurations are refactored by consuming applications, never migrated by
  BMForge.
- Add `manage.py verify` to check locally pinned skill and manager hashes
  without Git, network, cache freshness checks or writes, while leaving the
  original Git-based `check` for update discovery.
- Clarify current-spec-only adoption in agent guidance and lifecycle policy.

### Added

- Add realistic journal metadata fixtures and offline regression tests for
  native journal prefixes, fixed event names, IPv4/IPv6 and unit scoping, plus
  no-Git pin-integrity tests. Native live journal/Fail2ban acceptance remains
  required on a disposable systemd host.


## [0.21.2] - 2026-10-31 @ 17:44

### Summary

Separate application security-event publication from ban enforcement using
native systemd journald as the sole event channel. An application emits one
semantic event; Fail2ban, BMCyber and nftables retain their existing ownership
of native counting, local ban requests and kernel enforcement.

### Added

- Introduce optional `bmforge-security-events` with draft `0.1.0`
  specification, tiny stdlib-only Python producer asset, trusted request-context
  binding, fire-and-forget semantics and strict single-line journal formatting.
  The skill can be installed/attached independently without HTTP, ZMQ,
  Fail2ban or nftables.
- Add unit and pinned-skill regression tests covering isolated/nested/concurrent
  request contexts, IPv4/IPv6, invalid source/event injection, independent
  skill setup, offline asset pinning and update notifications.

### Changed

- Advance Fail2ban to draft `0.3.0`: native `backend = systemd`, unit-scoped
  `journalmatch`, explicit host journal dependencies, native per-IP
  `findtime`/`maxretry` and end-to-end tests from actual application requests
  rather than log-file fixtures. Keep the existing ZMQ prerequisite only in
  the blocking project, and leave kernel blocking unchanged.
- Advance HTTP to draft `0.5.1` with optional trusted client-source handling
  at the request boundary: verified proxy peers, overwritten headers,
  IPv4/IPv6 normalization and request-context isolation.
- Update the BMForge component catalogue, Codex entry-point guidance, manager
  bundle, blueprint, decision record and installation-independent acceptance
  workflow. Application repositories and production hosts remain untouched.


## [0.21.1] - 2026-10-31 @ 11:33

### Summary

Make the production Python virtual-environment contract enforceable by the BMForge
installer and explicit for all consuming application entry points, not just the
systemd service.

### Changed

- Advance the installation specification to draft `0.1.3`. Verify host
  `venv`/`ensurepip` prerequisites without requiring application packages
  globally, and use the installed Python environment for requirements,
  dependency checks and configured service/client imports.
- Track `venv_owned` before creation, reject unowned or checkout-backed
  environments and editable/development dependencies, and keep failed
  installation or upgrade attempts from advancing successful-version markers.
- Require the complete deployed runtime path in systemd, CLI/client launchers,
  Fail2ban actions and health probes. Runtime must work after the development
  checkout becomes unavailable; no new deployment framework is introduced.
- Expand lifecycle tests for read-only `--check`, dependency and import
  failures, environment ownership and cleanup, developer venv exclusion, and
  an offline pinned-wheel upgrade with checkout-independent imports.
- Correct the installation contract test's outdated bootstrap manager location.
- Clarify the BMForge-first repository boundary in agent guidance: consuming
  repositories are read-only references until their owners pin the new skill
  and request independent application changes.

## [0.21.0] - 2026-10-31 @ 10:35

This release is named for the element **Bohrium (Bh)**. Bohrium honors Niels Bohr, whose atomic model transformed our understanding of electrons.

### Summary

Isolate deployed Python dependencies under each application's `/opt/prod` installation instead of depending on a development checkout.

### Changed

- Advance installation specification to draft 0.1.2; add an opt-in production `.venv` to the existing installer template, with declared requirements installed before the successful-version marker.
- Require runtime service paths to use deployed Python and code, exclude source virtual environments, and document lifecycle and independence checks.


## [0.20.0] - 2026-10-31 @ 08:22

This release is named for the element **Rutherfordium (Rf)**.Rutherfordium honors 
Ernest Rutherford, whose experiments revealed the atomic nucleus.

### Summary

Give project documentation sites one reusable GitHub Pages standard, with shared
dark styling, required project branding and a concise, pinned site scaffold.

### Added

- Add optional `bmforge-github-pages` with draft `0.1.0` guidance, configuration,
  homepage/README/guide templates and publishing workflow. Bundle the complete
  resources for offline use through the existing skill manager without selecting
  application HTTP or Git components.

### Changed

- Require each site's own logo, consistent baseurl-aware navigation, wide content,
  author sidebar and front-matter titles without duplicate headings. Trim unused
  configuration boilerplate and document preserving existing sites on adoption.
- Restrict manual Pages workflow runs to `main` as well as push-triggered builds;
  keep scaffold Markdown out of BMForge's published pages.

## [0.19.1] - 2026-10-31 @ 05:50

This release is named for the element **Mendelevium (Md)**. Mendelevium honors Dmitri Mendeleev, whose periodic table anticipated the existence of several undiscovered elements.

### Summary

Keep timed blocking stateless in the service: Fail2ban requests a block, the
service chooses its duration, and the kernel holds and expires the entry.

### Changed

- Advance Fail2ban and nftables to draft `0.2.0`: use ban-only actions,
  accept repeated requests after restarts, and remove application source claims,
  saved deadlines, replay suppression and lifecycle tracking.
  Fail2ban ticket expiry and stop hooks leave enforcement untouched.

## [0.19.0] - 2026-10-31 @ 04:26

This release is named for the element **Fermium (Fm)**. Fermium was discovered 
in debris from the 1952 hydrogen-bomb test and named after physicist Enrico Fermi.


### Summary

Allow applications to use named local sockets for ZeroMQ request/reply messaging
while keeping the existing protocol, client behavior and TCP option.

### Changed

- Extend `bmforge-zmq` to draft `0.4.0` with configurable TCP or local IPC
  endpoints for clients, servers and health probes. Define filesystem access,
  single-instance startup, socket cleanup and consuming-project acceptance
  checks without new runtime modules or changes to the IP-only network schema.

## [0.18.0] - 2026-10-30 @ 20:41

### Summary

Add small, selectable skills for independent per-host blocking: application
security logs feed Fail2ban, a thin local ZMQ action requests bans, and nftables
enforces timed IP entries.

### Added

- Add optional `bmforge-nftables` and `bmforge-fail2ban` skills with draft 0.1.0
  contracts, focused runtime inventories and consuming-project acceptance checks.
  Scope them to owned timed ban sets and the native log/filter/jail/action path;
  leave broader tool features upstream.
- Require explicitly selected or already pinned ZMQ for Fail2ban before any
  installer writes. Keep nftables independently selectable and preserve existing
  pinned skills. Extend the catalogue, decision record and installer checks.

## [0.17.1] - 2026-10-30 @ 04:42

This release is named for the element **Actinium (Ac)**. Actinium-225 is being 
studied for targeted alpha-particle cancer therapies.

### Summary

Standardize local-time HTTP displays and MariaDB text comparison settings so
timestamps are consistent and cross-database SQL avoids collation mismatches.

### Changed

- Advance HTTP to draft `0.5.0`: display local `yyyy-mm-dd hh:mm:ss` timestamps
  with a 24-hour clock and no fractional seconds, using the application's local
  timezone consistently across server and browser views. Align timeline at
  `0.2.0`, preserving unambiguous API timestamps and UTC persistence.
- Advance DB Server to draft `0.5.0`: pin `utf8mb4` / `utf8mb4_unicode_ci` for
  database defaults, tables, character columns and canonical PyMySQL connections;
  require effective-setting checks and cross-database join validation on adoption.
  Existing application upgrades and data migrations remain deliberate operations.

## [0.16.0] - 2026-10-30 @ 03:00

This release is named for the element **Astatine (At)**. Astatine is so rare and radioactive that only tiny amounts exist naturally at any given moment.

### Summary

BMForge now defines a standard for editing timeline objects with vis-timeline, using the application's HTTP server and preserving application-owned validation and persistence.

### Added

- Add the optional `bmforge-timeline` skill and draft `bmforge.timeline` 0.1.0 contract, pinning vis-timeline 8.5.6 JavaScript/CSS with editing callbacks, acknowledged saves, locked objects, precise keyboard forms and explicit timezone rules.
- Require `bmforge-http` for timeline during init, attach and add; reject missing prerequisites before any writes and preserve an already pinned HTTP skill.

### Fixed

- Use real canonical templates in the bootstrap test fixture so release-scaffold checks can run instead of failing on placeholder constants.

## [0.15.0] - 2026-10-28 @ 17:40

This release is named for the element **Tantalum (Ta)**. Tantalum resists 
corrosion so well that it is used in demanding chemical equipment and electronic 
capacitors.

### Summary

Multi-service applications now have one standard command for starting and stopping
their services in sequence.

### Changed

- Require an executable `scripts/services start|stop` for applications with more
  than one service, using explicit command sequences without dependency awareness.
  Include the rule in pinned project guidance and generated agent instructions.

## [0.14.1] - 2026-10-28 @ 04:53

- Updated README.

## [0.14.0] - 2026-10-27 @ 04:12

This release is named for the element **Lanthanum (La)**. Lanthanum is used in 
specialized optical glass for camera lenses.

### Summary

Existing applications can now attach individual pinned BMForge skills without adopting
BMForge's greenfield architecture, release scaffolding or agent instructions.

### Added

- Introduce `manage.py attach --components` for established Git repositories: preserve existing `AGENTS.md`, application files and `.agents/` content; install only selected optional skills and the standard local pinning/check manager.
- Reuse `add` and offline `check` for attached projects, reject new-project branch setup, and cover preservation, conflicts, symlinks and partial-failure rollback with regression tests.
- Explain new-project versus existing-project workflows in the Codex skill and website documentation.

## [0.13.0] - 2026-10-26 @ 19:23

This release is named for the element **Barium (Ba)**. Barium compounds make 
some fireworks glow green, while barium sulfate is used as a contrast agent 
in medical imaging.

### Summary

Codex now requires a clear implementation go-ahead, so exploring a design or
agreeing on a specification cannot accidentally trigger code changes. The rule
is included in new projects through generated agent guidance and pinned skills.

### Changed

- Establish scope-bound implementation authorization across BMForge guidance,
  engineering contract, entry-point and project skills, and generated
  `AGENTS.md`. Allow read-only planning, recognize direct user requests without
  magic words, and require renewed approval for material deviations while
  keeping commit, release and deployment decisions separate.
- Add bootstrap regression checks for the generated authorization gate and
  notification-only updates to pinned engineering guidance.

## [0.12.3] - 2026-10-26 @ 05:20

This release is named for the element **Tellurium (Te)**. Tellurium is used in certain solar cells, particularly cadmium telluride photovoltaic panels.

### Summary

The concise Codex quick-start is now available in Ukrainian, and Ukrainian readers can reach it from the localized BMForge homepage. Agent-facing skills, commands and technical contracts remain in English.

### Added

- Translate the human-facing Codex quick-start into Ukrainian, with matching `translation_key`, a distinct localized permalink and a link back to the Ukrainian homepage.

### Fixed

- Link the Ukrainian homepage to its localized quick-start and remove the duplicate `# BMForge` heading where front matter already supplies the page title.

## [0.12.2] - 2026-10-26 @ 05:06

This release is named for the element **Antimony (Sb)**.  Antimony compounds are used in some flame-retardant formulations to help slow burning.

### Changed

- Website pages: Deleted headers where the title was the same (causes dupe display).

## [0.12.1] - 2026-10-26 @ 04:52

This release is named for the element **Tin (Sn)**. Tin has helped preserve food for centuries as a protective coating on steel cans.

### Summary

Codex now has one `$bmforge` entry point for new applications. Users install it once and select components through Codex; project-local pinning and setup remain handled by the skill.

### Changed

- Rename the user-level bootstrap from `bmforge-new-project` to `bmforge`, move its manager, update source paths and regression tests, and remove the old entry point without a compatibility alias.
- Reduce the public quick-start guide and homepage to installation and invocation instructions; keep component selection, branch setup and offline update management within the skill.
- Refresh the README, Ukrainian homepage and agent guidance to reflect implemented Codex skills and the correct installation locations.

## [0.12.0] - 2026-10-25 @ 16:14

This release is named for the element **Cadmium (Cd)**. Cadmium gives some pigments brilliant yellow and red colors, although its toxicity limits their use.

### Summary

Codex can now investigate production defects with the optional `bmforge-rca` skill: collect evidence over read-only SSH, then reproduce, debug and fix locally. Production hosts remain unchanged, and fixes follow the normal release and upgrade process.

### Added

- Add optional `bmforge-rca` to the pinned skill installer ([#16](https://github.com/NadimGhaznavi/bmforge/pull/16)), with SSH collection of logs and database dumps into local scratch storage. Require database queries, reproduction, debugging and fixes to run locally; prohibit remote file changes, SQL queries, service restarts and deployments during RCA. Include bootstrap regression coverage for pinned installation and notification-only update checks.

## [0.11.1] - 2026-10-25 @ 11:05

This release is named for the elemenbt **Rhodium (Rh)**.  Rhodium is prized in catalytic converters for helping reduce harmful vehicle emissions.

### Summary

Changelog maintenance is now mandatory for every completed project change, and meaningful improvements get a concise summary as they happen. The policy travels with pinned BMForge skills and newly generated agent instructions rather than relying on release-time reminders.

### Changed

- Require changelog entries for every completed logical change, including small code, test, documentation, configuration and maintenance work; use `### Summary` for individual meaningful improvements rather than only large releases.
- Embed the rule in the engineering contract, agent guidance, project skills, release documentation and the BMForge decision record.
- Advance HTTP Display Server to `0.4.0` with dark, saturated, high-contrast styling for human-facing GUIs; API-only services remain presentation-free.
- Bundle the changelog maintenance guide inside the pinned `bmforge-project` skill for offline use; existing projects retain their pinned guidance until explicitly updated.

### Added

- Cover generated changelog instructions and read-only detection of updated pinned changelog guidance in bootstrap regression tests.
- Pin BMDynIP's HTML/CSS from `2077300e7ee20de5328164115a277f353ed19579` for new HTTP skills, with spec and bootstrap regression checks.

## [0.11.0] - 2026-10-25 @ 05:51

This release is named for the element **Germanium (Ge)**. Germanium helped power the earliest transistors before silicon became the dominant semiconductor.

### Summary

BMForge skill update checks now work offline from a clean local `main` checkout. The check reports the cached revision, so `CURRENT` describes that snapshot rather than live GitHub freshness.

### Changed

- Use `~/.cache/bmforge-upstream` for `manage.py check`, with `BMFORGE_SOURCE` and `--source` overrides, without cloning or fetching; reject missing, dirty or non-`main` sources.
- Keep installed-skill integrity checks independent of source availability, preserving `LOCALLY MODIFIED` warnings when the cache is unavailable.
- Document cache creation, separate `git pull --ff-only` refreshes, local-source bootstrap and the `--source` workaround for older pinned managers; existing installations remain pinned until a user-approved upgrade.

### Added

- Add hermetic regression coverage for cached and unavailable offline checks, source validation, environment overrides and local modification reporting.

## [0.10.1] - 2026-10-25 @ 04:40

This release is named for the element **Zinc (Zn)**. Zinc protects steel from rust in galvanization by corroding preferentially to the iron beneath it.

### Added

- Link to osoyalce.com off the main index.md file.

### Fixed

- Correct the changelog's release-section grouping by consolidating duplicate `Fixed` headings in 0.10.0

## [0.10.0] - 2026-10-24 @ 22:43

### Added

- Introduce optional GIF Animation component (draft `bmforge.gif-animation` 0.1.0) with a Pillow encoder template, source-pinned Snake Web example, Codex skill, bootstrap integration and animation round-trip checks.
- Add a safe, read-only `setup-branches --dry-run` plus user-approved local `setup-branches` for the first `dev` and `feat/maint-0.1.0` branches after the project's initial commit; never commit or push automatically.
- Add bootstrap branch-safety regression tests and update the Codex runbook.

### Fixed

- Require ZeroMQ input validation to reject escaped lone Unicode surrogates without terminating a REQ/REP worker; add malformed-then-valid acceptance checks (draft ZMQ spec 0.3.1).
- Require role-and-operation-specific installation preflight, including accurate `--check` results for missing server provisioning commands (draft installation spec 0.1.1).
- Synchronize static PEP 621 `pyproject.toml` `[project].version` with application `VERSION` in the canonical release script and BMForge's own release script, rejecting drift before branch merges.
- Preserve tool-only `pyproject.toml` files and existing release-branch, tag, changelog and atomic-push behaviour; add release regression tests.
- Clarify that client-only installed CMDB metadata must not claim server-owned databases or listeners.


## [0.9.0] - 2026-10-24 @ 17:55

This release is named for the element **Titanium (Ti)**. Titanium combines high strength with low density and excellent corrosion resistance, making it valuable in aircraft and implants.


### Added

- Promote install/upgrade/uninstall completion to a **fourth mandatory greenfield skill** (`bmforge-installation`, draft spec 0.1.0), while keeping bootstrap itself deployment-disabled.
- Specify a standard installed version/CMDB identity under `/opt/prod/<project>`, including custom libraries and client-only installations.
- Specify optional client/server installation roles and role-preserving upgrades based on pinned DevLog examples; explicitly require a tested uninstall for every selected role.
- Add a minimal metadata-only installation lifecycle test, pinned DevLog role examples, contract tests and read-only skill update regression coverage.

### Changed

- Add component provenance to the existing generic file-installer template without changing its deployment algorithm or the release script.


## [0.8.2] - 2026-10-24 @ 17:19

This release is named for the element **Scandium (Sc)**. Small additions of scandium can make aluminium alloys stronger and lighter for aerospace applications.

### Added

- Bootstrap an executable project-specific `scripts/new-release.sh` by adapting the existing BMForge release template without changing its Git release workflow.
- Create its prerequisites from standard templates: version constants, changelog, CMDB checker and executable, deployment-disabled lifecycle scripts.
- Require a canonical application `--name`, refuse pre-existing or symlinked targets, and keep release-template updates notification-only.
- Add bootstrap tests for permissions, Bash syntax, exact template adaptation, metadata validity and read-only update checks.


## [0.8.0] - 2026-10-24 @ 15:10

This release is named for the element **Calcium (Ca)**. Known for it's presence in teeth and bones, it's also required to make your muscles move, to make your heart beat.

### Added

- Define separate draft constants (`bmforge.constants`) and runtime application localization (`bmforge.localization`) specifications and Codex skills.
- Pin source examples from Snake Lab and BMGeoIP for typed constant groups, and Minimal Mistakes plus the blog for language-selection and translation-display patterns.
- Provide an application-owned, standard-library `Localizer.py`, stable `DText` keys and an English JSON catalogue for new apps.
- Install constants and localization as part of the greenfield baseline, without auto-upgrading existing projects or changing the approval-only update policy.
- Add localization and bootstrap tests for locale resolution, translation fallback, protected placeholders, pinned assets and notification-only updates.


## [0.7.0] - 2026-10-24 @ 14:25

This release is named for the element **Potassium (K)**. Potassium is essential for nerve signals and muscle function, including keeping your heart beating normally.

### Added

- Add a global `bmforge-new-project` Codex bootstrap skill and six project-local skills for architecture, HTTP, ZeroMQ, MariaDB, Git and display visualizations.
- Add a pinned per-project skill manager and source-content lock file; read-only update checks report changes without applying updates.
- Add a concise greenfield skill setup guide and twelve hermetic tests for skill selection, pinning, safe installation and update notification.


## [0.6.0] - 2026-10-24 @ 13:45

This release is named for the element **Argon (Ar)**. Argon takes up nearly 1% of the air we breathe and is used to shield welds from unwanted chemical reactions.

### Added

- Document the USDP-inspired Activity / Interface / Entity classification and package responsibility rules.
- Supply a canonical application-independent MariaDB `DbMgr.py` to copy verbatim into consuming apps, with unit tests for connections, transactions, read-only mode and application-mediated health.
- Pin MyCount Activity (`CollectVisit`), Interface (`VisitDb`) and Entity (`Visit`) files to illustrate real usage of the classification.
- Define an optional display-visualization component with approved browser libraries: Plotly.js 4.1.1 for plots, Leaflet 1.9.4 for maps, and Cytoscape.js 3.34.3 for network/relationship graphs.
- Pin unchanged MyCount and CMDB visualization reference files and locally bundle the approved Cytoscape.js artifact and licence for reuse.
- Document capability selection, fixed versions, Codex approval boundaries and rendering acceptance checks separately from the Python HTTP component.

### Changed

- Specify the layered database access pattern: `activity` → domain `interface/*Db` → `interface/DbMgr` → MariaDB, with entities passed through layers.
- Advance draft DB Server specification to `0.4.0`; DB connection settings are resolved by each app and injected, with no app-specific imports in the manager.

## [0.5.0] - 2026-10-24 @ 12:25

### Added

- Specify the exact approved runtime modules and their roles for HTTP Display Server, ZeroMQ REQ/REP, and DB Server.
- Require Codex to obtain approval and revise the component specification before adding or substituting infrastructure libraries.
- Introduce a `Git` component (`bmforge.git`, draft spec 0.1.0) with two operations: managed-file publishing and repository-wide add/commit/push.
- Copy the original Snake Web `GitPublisher` into a pinned local snapshot; provide a standalone Git CLI template and local Git integration tests.

### Changed

- Advance the three draft component specifications to `0.3.0`; keep component-specific technology choices separate from application business logic.

## [0.4.1] - 2026-10-24 @ 10:54

This release is named for the element **Phosphorus (P)**. Phosphorus was first isolated from urine in 1669 by an alchemist searching for the philosopher's stone. (Maybe it should be called **Phoolorus**?).

## [0.4.0] - 2026-10-24 @ 10:32

This release is named for the element **Silicon (Si)**. Silicon is the backbone of modern computer chips and is the second most abundant element in Earth's crust.

### Added

- Specify simple, on-demand application health checks for HTTP, ZeroMQ, and application-mediated DB Server monitoring; CMDB sees green/red without direct MariaDB access.
- Establish the lean, fail-fast engineering contract and specification traceability policy for component-owning modules.
- Record BMForge architecture decisions and explicitly track Codex skills and CMDB component scanning as future work.

### Changed

- Advance the three draft component specifications to `0.2.0` for the new health-check contract.
- Name the database component `db-server` while retaining its MariaDB implementation contract.
- Reorganize the website for task-first Codex navigation and mark the initial HTTP, ZeroMQ, and MariaDB contracts as draft version 0.1.0.

## [0.3.0] - 2026-10-21 @ 03:47

This release is named for the element **Boron (B)**. Boron compounds help give heat-resistant borosilicate glass its remarkable durability!

### Changed

- Document the runtime configuration contract for future applications: constants supply defaults, production JSON supplies persistent overrides, and shared resolution supports application tools and CMDB discovery.
- Align CMDB compliance with current metadata, scan, persistent component, database, and backup behavior; accept software classifications without a fixed vocabulary while recommending `application` for new projects.
- Add a network configuration process covering literal listener defaults, shared runtime resolution, production overrides, installation, restart, and deployment verification, with CMDB network discovery explicitly pending.
- Add empty listener declarations to starter and BMForge constants and validate declared listener roles, IPv4 addresses, and ports in both metadata checkers.

## [0.2.0] - 2026-10-19 @ 04:35

The **Rosetta** release is named for the *ESA comet exploration mission*.

### Added

- A standard install, upgrade, and uninstall contract with guarded starter scripts for new projects.
- BMForge file deployment under `/opt/prod/bmforge`, including readable CMDB metadata, managed-file ownership, retained unowned files, and a successful-version marker.

### Changed

- Require executable, committed install, upgrade, and uninstall entry points during release preflight.

## [0.1.0] - 2026-10-19 @ 04:06

The **Queqiao** release is named for the *Chinese lunar communications relay*.

### Summary

Establish BMForge as a shared development reference for coding agents working on new and existing projects. Provide focused processes and reusable templates for documentation, CMDB compliance, maintenance, and releases.

### Added

- Jekyll configuration and GitHub Pages publishing guides and templates.
- Multilingual documentation guidance, with English metadata prepared during setup and translation deferred until project completion.
- CMDB naming, installation, and metadata standards, including the required `CMDB_TYPE = "Application"`, a constants template, and a metadata checker.
- Release setup and publishing processes, a reusable release script, and optional deployment impact tracking with tests in disposable projects and local Git remotes.
- A day-to-day changelog maintenance process covering unreleased entries, summaries, and the handoff to release tooling.
- BMForge's own CMDB constants, metadata checker, and release script, using the shared templates.

### Changed

- Organize documentation by task, with separate guides linked from the project index.

---

[Back]({{ site.baseurl }}{% link index.md %})


