---
title: Changelog
lang: en
locale: en-US
language_name: English
translation_key: bmforge-changelog
permalink: /CHANGELOG/
---

## [Unreleased]

This release is named for the element **Boron (B)**. Boron compounds help give heat-resistant borosilicate glass its remarkable durability!

### Changed

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
