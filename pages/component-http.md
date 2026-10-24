---
title: HTTP Display Server Component
lang: en
locale: en-US
language_name: English
component_id: "bmforge.http-server"
spec_version: "0.1.0"
spec_status: "draft"
translation_key: bmforge-component-http
---

# HTTP Display Server

**Component ID:** `{{ page.component_id }}` · **Specification:** `{{ page.spec_version }}` ({{ page.spec_status }})

This contract follows the [engineering policy]({{ site.baseurl }}{% link pages/engineering-contract.md %}) and [traceability rules]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}).

## Intent and scope

Provide a small, locally owned HTTP service using Python's `ThreadingHTTPServer`, `BaseHTTPRequestHandler`, and (when HTML is needed) Jinja2 templates with autoescaping. Do not introduce Flask, FastAPI, a frontend build, authentication framework, or extra infrastructure unless required by the consumer.

## Reference snapshot

- `components/reference/bmgeoip/bmgeoip/server/BMGeoIPServer.py`: listener, CLI binding, integration, lifecycle
- `components/reference/bmgeoip/bmgeoip/server/BMGeoIPHandler.py`: GET/HEAD/POST routing, templates, JSON response, health endpoints

These contain GeoIP-specific routes, data-loader integration, globals, and filenames. **Do not reproduce those behaviours** in unrelated applications.

## Required contract

- The application supplies the server class/entry point, request handler, routes, and service dependencies.
- Read listener defaults from the application's declared network constants and production overrides; optionally allow explicit CLI overrides. Validate host and port before bind. Publish the listener in `CMDB_NETWORK` and use the Network Configuration process.
- Use a bounded request socket timeout. Bind failure and fatal worker failure must surface as errors; do not claim readiness before successfully binding.
- Implement `GET`, `HEAD`, and only the required mutation methods. A HEAD request sends headers but no body. Unknown routes return 404.
- Return accurate status codes, `Content-Type`, UTF-8 where applicable, `Content-Length`, `Cache-Control: no-store` where appropriate, and `X-Content-Type-Options: nosniff`.
- For JSON writes, validate method, path, Content-Type, request length, schema, and user-supplied fields; reject malformed or oversized requests with 4xx rather than uncontrolled exceptions. Consider origin/access policy for state-changing endpoints; same-origin checks are not authentication.
- Use Jinja2 HTML autoescaping and fail on missing template values; keep templates, static assets and route data application-owned. Never embed secrets in rendered output or public diagnostics.
- Implement `/health` (process alive) and `/ready` (service capable of serving its essential dependencies). If they differ, readiness must actually check dependencies rather than return a fixed success.
- Cleanly close the HTTP listener and any owned background workers during termination, including SIGTERM. No orphaned threads.
- Keep application-specific business logic out of the generic HTTP mechanics. Use typed interfaces or injected collaborators where useful without inventing extra layers.

## Acceptance checks

1. Bind to a test loopback address and ephemeral port; GET known path returns correct body, type and length; HEAD omits body.
2. Unknown route is 404; unsupported mutation and malformed/oversized JSON do not crash the server.
3. HTML user-provided values are escaped; static assets cannot traverse outside allowed paths.
4. `/health` and `/ready` follow documented semantics during normal operation and simulated dependency failure.
5. Address-in-use, invalid port and graceful shutdown are tested; service exits without lingering workers.
6. Confirm the installed application exposes its declared address/port, respects production overrides, and has no runtime import of BMForge/bmgeoip.
