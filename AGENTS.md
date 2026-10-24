# BMForge agent guidance

BMForge is an independent repository of software-development standards, component specifications, and pinned reference implementations. It is **not** a shared runtime library.

For component-driven tasks:

1. Read `pages/component-blueprints.md`, then only the requested component pages in `pages/component-{http,zmq,database}.md`.
2. Read their **local**, version-pinned examples under `components/reference/bmgeoip/` for tested patterns. Do not visit or import the original project to obtain implementation code. The reference files intentionally contain application-specific code and may not run in isolation; adapt them, do not copy unrelated business logic.
3. Implement and maintain the code in the destination application's own package. Never add BMForge or a source-example project as a runtime dependency. Separate applications may interact using documented public APIs.
4. Use existing BMForge runtime configuration, network configuration, CMDB discovery, installation and release standards. Do not duplicate those standards in new components.
5. Verify the component's acceptance checklist with application-local tests. Make errors visible; do not report an untested installation as complete.
6. Avoid speculative services, abstractions and features beyond the application's declared scope. If an architectural choice would substantially expand scope, ask before implementing it.

Reference provenance and update policy are documented on `pages/component-blueprints.md`. Changes to the pinned snapshots require an intentional review and matching specification/test updates.
