# BMForge agent guidance

BMForge is a **standalone engineering specification repository**, not a runtime library. Every application owns its implementation.

## Read only what the task needs

1. Read `pages/engineering-contract.md` first. Build the smallest clear implementation that satisfies the requirement, and fail visibly when internal contracts cannot be met.
2. Use `index.md` to find the relevant process. For components, read `pages/component-blueprints.md` and only the selected `pages/component-{http,zmq,database}.md` specifications.
3. Use the **local, pinned** source examples under `components/reference/bmgeoip/`. Do not fetch moving bmgeoip source or transplant unrelated GeoIP functionality.
4. Follow existing BMForge configuration, CMDB, install, and release processes when those concerns apply. Never add BMForge or an example project as a runtime dependency. Independent applications interact through documented public APIs.
5. When creating a BMForge-derived component, apply the literal source marker specified in `pages/specification-lifecycle.md`, using the selected specification's ID and version.
6. Run the component's acceptance checks in the destination project and report what actually passed, failed, or was not tested. A copied example is not a completed component.

## Engineering rules

- Validate untrusted inputs at external boundaries. Trust established internal contracts instead of repeating defensive checks.
- Don't swallow exceptions or invent fallbacks, retries, workers, queues, abstractions, or optional features. Include additional complexity only for a named requirement or observed failure.
- A critical distributed operation needs its defined result, timeout, and error semantics. Never claim success before it is known.
- A failed required dependency or unexpected internal state must surface clearly. Gracefully reject invalid external requests without disguising internal defects.
- When improving BMForge, distinguish implementation bugs from contract gaps. Update acceptance checks and specification versions intentionally; record policy-level decisions in `DECISIONS.md`.
- Ask before materially expanding an application's scope. This project is not a licence to build unrequested infrastructure.

For current status and unresolved work, read `DECISIONS.md`. Skills and CMDB component scanning are planned, not yet present.
