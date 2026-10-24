# BMForge

Engineering standards, component specifications, and frozen reference implementations for Codex-driven projects. **No shared runtime code.**

- Start with [AGENTS.md](AGENTS.md) and the [engineering contract](pages/engineering-contract.md).
- [Install Codex component skills](pages/codex-skills.md) from the global bootstrap, then use the reviewed, post-commit `setup-branches` action to create local `dev` and initial feature branches; constants, localization and a configured `scripts/new-release.sh` release scaffold are included, with read-only update notices.
- Read the distinct [constants](pages/component-constants.md), [runtime localization](pages/component-localization.md) and [installation lifecycle](pages/component-installation.md) specifications. Every installed project gets a versioned `BASE_DIR`, even a CLI or custom library.
- Find tasks and website documentation in [index.md](index.md).
- Build using the [component blueprints](pages/component-blueprints.md) and their pinned local examples.
- Organize new application classes with [Activity / Interface / Entity](pages/classification.md), and reuse the canonical MariaDB manager from [DB Server](pages/component-db-server.md).
- Choose [approved visualization libraries](pages/component-visualization.md) deliberately for charts, maps and relationship graphs.
- See [specification traceability](pages/specification-lifecycle.md) and [recorded decisions](DECISIONS.md).

The website is published at https://bmforge.osoyalce.com. The component specifications are drafts requiring validation in consuming applications; native skills and CMDB component scanning are planned, not yet implemented.
