# BMForge agent guidance

BMForge is a **standalone engineering specification repository**, not a runtime library. Every application owns its implementation.

## Read only what the task needs

1. Read `pages/engineering-contract.md` and `pages/classification.md` first. Build the smallest clear implementation that satisfies the requirement, and fail visibly when internal contracts cannot be met.
2. Use `index.md` to find the relevant process. For components, read `pages/component-blueprints.md` and only the selected `pages/component-{http,zmq,db-server}.md` specifications.
3. Treat each selected component specification's **Approved runtime modules** section as a fixed implementation inventory. Copy/adapt only from that list. If it cannot meet the requirement, **pause and ask the user before adding packages or changing technologies**; don't silently swap in another framework.
4. Use locally pinned reference examples for understanding, not runtime imports. HTTP/ZeroMQ may adapt `components/reference/bmgeoip/`; **DB Server must copy `components/templates/db-server/interface/DbMgr.py` unchanged**, passing app configuration and implementing domain `*Db` interfaces around it. Never fetch moving examples or transplant source-app business logic.
5. Follow existing BMForge configuration, CMDB, install, and release processes when those concerns apply. Never add BMForge or an example project as a runtime dependency. Independent applications interact through documented public APIs.
6. When creating a BMForge-derived component, apply the literal source marker specified in `pages/specification-lifecycle.md`, using the selected specification's ID and version.
7. For a running application, implement the on-demand checks in `pages/health-checks.md` using existing HTTP/ZeroMQ interfaces and the application's own DB layer. Never give CMDB direct MariaDB access.
8. Run the component's acceptance checks in the destination project and report what actually passed, failed, or was not tested. A copied example is not a completed component.

## Engineering rules

- Classify substantial classes explicitly: `activity/` orchestrates work, `interface/` owns external and domain data access, `entity/` carries data. Domain `*Db` classes compose with the unchanged `DbMgr`. Do not put SQL in activity or entity classes.
- Validate untrusted inputs at external boundaries. Trust established internal contracts instead of repeating defensive checks.
- Never introduce a new module, server framework, database driver, ORM, plotting library, or dependency to replace an approved component implementation without explicit user approval and a specification update.
- Don't swallow exceptions or invent fallbacks, retries, workers, queues, abstractions, or optional features. Include additional complexity only for a named requirement or observed failure.
- A critical distributed operation needs its defined result, timeout, and error semantics. Never claim success before it is known.
- A failed required dependency or unexpected internal state must surface clearly. Gracefully reject invalid external requests without disguising internal defects.
- When improving BMForge, distinguish implementation bugs from contract gaps. Update acceptance checks and specification versions intentionally; record policy-level decisions in `DECISIONS.md`.
- Ask before materially expanding an application's scope. This project is not a licence to build unrequested infrastructure.

For Git publishing or commits, read `pages/component-git.md` and copy `components/templates/git/Git.py` into the application's own namespace. Use only its approved modules. The frozen Snake Web `GitPublisher.py` is a source reference, not a runtime dependency. Do not invent release automation, switch Git libraries, or alter the prescribed commit commands.

For current status and unresolved work, read `DECISIONS.md`. Skills and CMDB component scanning are planned, not yet present.
