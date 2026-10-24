---
title: DB Server Component
lang: en
locale: en-US
language_name: English
component_id: "bmforge.db-server"
spec_version: "0.2.0"
spec_status: "draft"
translation_key: bmforge-component-db-server
---

# DB Server

**Component ID:** `{{ page.component_id }}` · **Specification:** `{{ page.spec_version }}` ({{ page.spec_status }})

This contract follows the [engineering policy]({{ site.baseurl }}{% link pages/engineering-contract.md %}), [health check contract]({{ site.baseurl }}{% link pages/health-checks.md %}), and [traceability rules]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}).

## Intent and scope

Provide a minimal application-owned database service layer backed by MariaDB using PyMySQL. This is application-side data access, not a managed MariaDB daemon. Separate connection/SQL execution mechanics from application schema and queries. Do not introduce an ORM, global connection pool, migration framework or remote service without a concrete requirement.

## Reference snapshot

- `components/reference/bmgeoip/bmgeoip/interface/DbMgr.py`: owned PyMySQL connection, bound execution, query and rollback/commit
- `components/reference/bmgeoip/bmgeoip/interface/DatabaseEnvironment.py`: database configuration loader
- `components/reference/bmgeoip/bmgeoip/interface/GeoIpDb.py`: **application-specific example only**, showing schema creation, bounded import batches and atomic updates

## Required contract

- The application's DB manager owns one connection, opened from protected application configuration and closed deterministically. Never pass a connection between concurrent worker threads; make each worker acquire its own connection.
- Use configurable host/port or Unix socket, schema name, username and secret; no credentials in source, public documentation, status messages or HTTP output. Validate required fields and file permissions where applicable.
- Use utf8mb4, dictionary results as needed, explicit connect/read/write timeouts, and strict SQL mode consistent with the reference implementation.
- Provide the small operations actually required: parameterised `execute`, `execute_many`, `query`, `transaction` and `close`. Use driver-bound parameters for all values; never interpolate untrusted data into SQL. Validate unavoidable identifiers against a known allowlist.
- Transaction context commits only on success and rolls back on exceptions, preserving the original exception even when rollback also fails. DDL and schema creation are handled separately from multi-statement data transactions.
- The application-specific repository/data class owns SQL schema, indexes, unique constraints, read/write methods and atomic workflows; **do not import GeoIpDb or create GeoIP tables** for another application.
- Offer a small application-internal, read-only health operation using the **application's configured database connection** (for example `SELECT 1` via its DB manager). It reports failure when the app cannot use that connection; do not catch and suppress errors, reconnect automatically, or create a special monitoring connection. The application's health handler reports this result to CMDB; **CMDB must not connect to MariaDB directly for DB Server health**.
- Use `CMDB_DATABASES` declarations for app discovery and follow BMForge runtime configuration and deployment guidance. An inventory declaration does not create database users, schema or backups automatically.
- Explicitly choose the consistency and concurrency contract for each application's writes. For a time-tracking service, consider idempotent event IDs and transactional session transitions only when those behaviours are part of its own requirements.

## Acceptance checks

1. Connect with a dedicated test database and credentials; missing/bad credentials fail without exposing passwords.
2. Bound insert/query round trip works, including Unicode and parameterised values; injection-like input is stored as a value.
3. Multiple writes commit atomically; an injected failure rolls all writes back and rethrows.
4. Separate worker threads use separately owned connections; closure releases resources.
5. Invalid/missing configuration and a database outage yield explicit errors and do not leave a partially reported success.
6. Application-internal DB health succeeds while the app can query through its own connection, fails on a simulated outage, and causes the application's aggregate `/health` to become unhealthy; no direct CMDB-to-MariaDB connection is used.
7. Only the new application's schema and SQL are present; no BMForge/bmgeoip runtime imports. Verify CMDB declarations agree with deployment.
