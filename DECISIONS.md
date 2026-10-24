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

**Current scope.** HTTP, ZeroMQ REQ/REP, and DB Server (MariaDB-backed) contracts are draft `0.2.0` specifications with locally pinned bmgeoip examples. DevLog will test whether the contracts are sufficient.

## 2026-10-24: minimal application health checks

**Monitoring.** Running applications answer on-demand health checks through their existing HTTP or ZeroMQ interface. HTTP `GET /health` returns `200` (green) or `503` (red) and identifies required component failures. The DB Server check runs inside the application on its configured connection; CMDB never logs into MariaDB for this check. No dedicated health service, background polling, retry engine, or self-recovery architecture. See `pages/health-checks.md`.

## Work not yet implemented

- Package component and project workflows as native Codex skills. Keep one authoritative contract per component and include all required local references.
- Implement CMDB-side polling of application health endpoints and simple red/green reporting; BMForge defines the application contract only.
- Add optional static CMDB component discovery and comparison reporting. Do not conflate architectural component metadata with `CMDB_COMPONENTS` filesystem backup declarations.
- Validate the three contracts through DevLog, then publish immutable specification revisions and improve only the gaps the implementation exposes.

## Changing a decision

When a new requirement changes an engineering principle or architectural boundary, update the relevant contract and amend this record with the reason. Keep historical decisions visible rather than silently rewriting their rationale.
