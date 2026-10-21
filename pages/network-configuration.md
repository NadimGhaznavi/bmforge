---
title: Network Configuration
lang: en
locale: en-US
language_name: English
translation_key: bmforge-network-configuration
---

Use `CMDB_NETWORK` as the single source for application listener defaults. This process follows CMDB's [network developer guide](https://github.com/NadimGhaznavi/cmdb/blob/main/pages/cmdb-network.md), reviewed against `/opt/dev/cmdb/pages/cmdb-network.md` on 2026-10-21. The application standard is available now; CMDB collection, storage, and display remain pending.

## Declare Defaults

Place a direct literal in the existing constants file from [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}). For a fictional Example application:

```python
CMDB_NETWORK = (
    ("http", "0.0.0.0", 18080),
    ("backend", "127.0.0.1", 18081),
)
```

Each entry is a literal `(use, interface, port)` tuple. `use` is a unique, nonempty role name that remains stable for configuration and consumers. Use names without surrounding whitespace. `interface` is an IPv4 address string. `port` is an integer from 1 to 65535; booleans and strings are invalid. Annotated assignments are supported. Use `CMDB_NETWORK = ()` when there are no listeners.

Declare all listeners owned or configured by the application, including internal services and managed proxies. Keep outbound database and other dependency connection settings separate; database inventory references belong in `CMDB_DATABASES`. Keep credentials out of the declaration and network JSON. Hostnames, IPv6, Unix sockets, and transport-specific extensions are outside the current pattern; `use` names the role and supplies no separate transport field.

## Resolve Runtime Settings

Implement a shared configuration interface and network resolver following CMDB and MyCount's `Configuration` and `Network` pattern. Resolve by role, for example `Network.binding("http")`, returning `(interface, port)`. Replace tuple-position lookups, duplicate fallback values, and older listener constants. A copied constants declaration alone does not wire the application's listeners.

Route server startup, managed proxy listeners and upstreams, installation health checks, and router mapping creation and cleanup through this resolver where those consumers exist. Local clients use `Network.destination(use)`, which substitutes `127.0.0.1` for a wildcard bind address of `0.0.0.0` and preserves specific addresses.

Use this precedence, from lowest to highest:

1. Literal `CMDB_NETWORK` defaults.
2. Production JSON overrides in `/opt/prod/<lowercase-name>/conf/<lowercase-name>.json`.
3. Supported command-line overrides for that invocation.

A partial Example configuration is:

```json
{
  "network": {
    "http": {
      "interface": "127.0.0.1",
      "port": 19080
    }
  }
}
```

A missing file uses defaults. Omitted roles and fields inherit defaults. Reject malformed JSON, unknown roles or fields, invalid IPv4 addresses, and invalid ports with an error identifying the file or setting. Invalid configuration must fail instead of silently using defaults. Resolve configuration once per process and restart affected processes after edits. Preserve existing supported CLI overrides.

The declaration describes default inventory. Production JSON and CLI overrides can change actual bindings without changing the declaration. Current CMDB scans cannot verify either declared or effective network settings.

## Integrate Installation and Restart

Extend the project's [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) to create readable production JSON from the declaration only when the file is missing. Preserve existing configuration on reinstall and upgrade. Validate it before stopping services. Retain live configuration during uninstall under BMForge's lifecycle contract unless the project explicitly documents another policy.

Provide a restart entry point for applications with services. Validate configuration first, then apply all affected settings, including generated proxy configuration or router mappings where present. Health checks must use the same resolved settings as the services. Complete and verify this project-specific work before enabling the starter installer's `DEPLOYMENT_READY` flag; the starter does not provide a runtime resolver or manage network JSON.

Include the resolver, configuration defaults, restart tooling, proxy templates, and related health checks in [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) when enabled.

## Verify the Application

- Run the metadata checker to validate the literal declaration. It accepts an omitted declaration for existing projects and validates one when present.
- Change declared defaults in a test and confirm server, proxy, health-check, and router consumers use the new bindings where applicable.
- Check missing and partial JSON configurations and CLI precedence.
- Check that malformed JSON, unknown settings, invalid addresses, and invalid ports fail before service stops or restart actions.
- Verify reinstall and upgrade preserve production configuration and that restart applies edits to all affected consumers.
- Remove replaced constants and hardcoded listener defaults. Check effective bindings and health after deployment separately from CMDB discovery.

---

[Back]({{ site.baseurl }}{% link index.md %})
