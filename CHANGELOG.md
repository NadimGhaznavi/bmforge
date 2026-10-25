---
title: Changelog
lang: en
locale: en-US
language_name: English
translation_key: bmforge-changelog
permalink: /CHANGELOG/
---

## [Unreleased]

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
