BMForge’s skills are **a pinned engineering rulebook for building Python applications**. They combine instructions, specifications, templates, frozen reference code, and acceptance checks. Each application owns its implementation; BMForge is not imported as a runtime framework.

This repository contains nine project-local skills:

| Skill | What it governs |
|---|---|
| [bmforge-project](/opt/dev/devlog/.agents/skills/bmforge-project/SKILL.md) | Architecture: activities coordinate work, interfaces handle external systems and domain access, entities hold data. |
| [bmforge-constants](/opt/dev/devlog/.agents/skills/bmforge-constants/SKILL.md) | Domain-grouped constants and stable identifiers using `Final` and enums. |
| [bmforge-localization](/opt/dev/devlog/.agents/skills/bmforge-localization/SKILL.md) | English message catalogues from the first UI feature, request-specific locale selection, and translations only when requested. |
| [bmforge-installation](/opt/dev/devlog/.agents/skills/bmforge-installation/SKILL.md) | Working install, upgrade, and uninstall operations, including version and ownership records under `/opt/prod`. |
| [bmforge-http](/opt/dev/devlog/.agents/skills/bmforge-http/SKILL.md) | Python’s `ThreadingHTTPServer`, optional Jinja2 templates, and on-demand health checks. |
| [bmforge-zmq](/opt/dev/devlog/.agents/skills/bmforge-zmq/SKILL.md) | PyZMQ REQ/REP messaging with explicit methods, bounded failures, and protocol validation. |
| [bmforge-db-server](/opt/dev/devlog/.agents/skills/bmforge-db-server/SKILL.md) | MariaDB access through an unchanged canonical `DbMgr.py`, with application-specific SQL in domain interfaces. |
| [bmforge-git](/opt/dev/devlog/.agents/skills/bmforge-git/SKILL.md) | Repository-wide commit/push and controlled publication of managed files. |
| [bmforge-visualization](/opt/dev/devlog/.agents/skills/bmforge-visualization/SKILL.md) | Browser charts with Plotly.js, maps with Leaflet, and relationship graphs with Cytoscape.js at approved versions. |

The first four are mandatory for new applications. The remaining components are selected from actual requirements.

There is also a user-level [bmforge-new-project](/home/dan/.codex/skills/bmforge-new-project/SKILL.md) skill. It bootstraps a repository with selected skills, pinned references, version metadata, and release and installation scaffolding. The installation stubs must then be completed and tested for the application’s actual topology.

The overall philosophy is **the smallest clear implementation that meets the requirements**: ordinary composition, clear responsibility boundaries, validation at external inputs, visible failures, and meaningful tests. Approved technologies are binding; adding a framework, changing a database driver, or upgrading a component requires explicit authorization. Installing a skill also does not authorize commits, releases, or deployment.

Your [lock file](/opt/dev/devlog/.agents/bmforge/lock.json) pins these skills to BMForge revision `7047662`. I ran the read-only offline update check, but it could not determine update availability because `~/.cache/bmforge-upstream` is missing. No files or skills were changed.
