---
title: Component Blueprints
lang: en
locale: en-US
language_name: English
translation_key: bmforge-component-blueprints
---

# Component Blueprints

BMForge is a **standalone specification and reference-code repository**, not a shared runtime library, package registry, or framework dependency. A new application owns its generated/copied code. Do not import BMForge or another project's Python modules in production. Cross-project integration is permitted only via the other project's explicitly documented public API.

## Codex workflow

1. Select only the components requested by the application's requirements. Read each specification in full.
2. Use the pinned code under `components/reference/bmgeoip/` as a **local reference snapshot**. Inspect it without fetching upstream repositories. Adapt and copy the necessary implementation into the new application's namespace. The snapshot intentionally contains application-specific details, not a drop-in generic library.
3. Replace BMGeoIP-specific names, routes, configuration, schema, message methods, resource paths, and lifecycle hooks. Do not copy GeoIP business functionality into an unrelated application.
4. Follow BMForge's existing runtime/network configuration, installation, and CMDB processes. The project owns its configuration, service units, tests, database schema, and deployment.
5. Implement the acceptance checks in each chosen specification. Test failure handling, startup/shutdown, and real boundaries. Report checks run and any deviations.
6. Avoid speculative infrastructure, layers, dependencies, and features. Ask before broadening scope.

## Blueprints

- [HTTP Display Server]({{ site.baseurl }}{% link pages/component-http.md %})
- [ZeroMQ Request/Reply Server]({{ site.baseurl }}{% link pages/component-zmq.md %})
- [MariaDB Data Access]({{ site.baseurl }}{% link pages/component-database.md %})

## Reference provenance

The vendored example files in `components/reference/bmgeoip/` are copied from `NadimGhaznavi/bmgeoip` at commit `35c8745c7003a124dce5b5799b08b2d7c851fbfc` (24 October 2026). They are immutable examples from that revision, not live links, and must not be periodically synchronised without review. The source file layout is retained to show component boundaries and imports. Some examples depend on BMGeoIP-only modules intentionally not part of the component catalogue; implementation agents must replace those integrations, not attempt to run the snapshot as a standalone application. External library dependencies (Python standard library, pyzmq, PyMySQL, Jinja2) remain explicit installation requirements of the **generated application's** chosen components.

## Component boundaries

The HTTP server owns request/response mechanics; application handlers own routes, HTML, API behaviour and policy. The ZMQ transport owns socket/message lifecycle; application handlers own command semantics. The database manager owns connection/transaction mechanics; application data access owns tables and SQL. Do not make these components depend on one another unless the new application's explicit data flow requires it.

**Completion rule:** a component is delivered only after it runs and passes its specified acceptance checks in the consuming project. Documentation or copied files alone do not qualify.
