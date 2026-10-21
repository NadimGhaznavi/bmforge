---
title: Runtime Configuration
lang: en
locale: en-US
language_name: English
translation_key: bmforge-runtime-configuration
---

Give applications a predictable configuration file so operators can adjust a deployment without editing source code and CMDB can discover its runtime settings. Use the same defaults and override rules for application startup, operational tools, and discovery.

## Establish the Configuration Contract

Store deployment-specific settings in `/opt/prod/<lowercase-name>/conf/<lowercase-name>.json`, using the canonical name from [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}). Resolve this path from the application's installation root, independently of the caller's working directory. A `CONFIG_FILE` constant can declare the relative path, for example `conf/bmgeoip.json`.

Keep shipped defaults in the project's constants file. Keep operator overrides in JSON. Changing one deployment's settings must not require editing its constants file or creating a new release. Release metadata such as `VERSION` and `CMDB_CODENAME` remains in constants and is not runtime configuration.

Document each supported setting, its JSON key, type, default constant, validation rules, and when changes take effect. Group related settings under named objects, such as `network`. Use stable keys so operators, application tools, and CMDB share one interpretation.

## Resolve Defaults and Overrides

Apply settings in this order, from lowest to highest precedence:

1. Shipped defaults from the constants file.
2. Overrides from the production JSON file.
3. Supported command-line overrides for that invocation.

A missing file uses defaults. A partial file overrides only the supplied settings; omitted groups and fields inherit their defaults. Treat an explicit value as an override even when it matches the current default. It remains fixed if a later release changes that default. Document this distinction when generating a complete initial file: populated values become deployment settings, while omitted values follow future defaults.

Implement one shared configuration interface that reads, validates, and resolves these settings. Application consumers must use that interface instead of duplicating fallback values or reading JSON independently. Route service startup, workers, generated service configuration, restart tools, and health checks through the same resolution rules where applicable.

Reject malformed JSON, unknown keys, incorrect types, and invalid values. Identify the file and setting in errors. Only a missing file falls back to defaults; unreadable or invalid files must fail clearly. Validate the file even when invocation overrides supply the affected settings.

## Example: BMGeoIP Listeners

BMGeoIP declares listener defaults in `bmgeoip/constants/DBMGeoIP.py`:

```python
CMDB_NETWORK = (
    ("http", "0.0.0.0", 54300),
    ("zmq", "0.0.0.0", 54301),
)
CONFIG_FILE = "conf/bmgeoip.json"
```

An operator can supply `/opt/prod/bmgeoip/conf/bmgeoip.json`:

```json
{
  "network": {
    "http": {"interface": "127.0.0.1", "port": 54310},
    "zmq": {"interface": "127.0.0.1"}
  }
}
```

The resolved HTTP binding is `127.0.0.1:54310`. The ZMQ binding is `127.0.0.1:54301`, inheriting its port from constants. Without the file, both listeners use their declared defaults. A supported HTTP port argument overrides `54310` for that invocation without modifying either file.

Follow [Network Configuration]({{ site.baseurl }}{% link pages/network-configuration.md %}) for listener declarations, address and port validation, and binding versus client destination resolution. Other configurable features follow the same constants-to-JSON relationship with their own documented schema.

## Make Settings Discoverable

Keep the installed constants and non-secret JSON readable by the CMDB inventory account, with directory traversal access. JSON is data: discovery must not need to import application modules, execute application code, or source shell files to interpret deployment overrides.

The discovery contract combines shipped defaults with JSON overrides using the same schema and precedence as the application. The constants describe the release's defaults; JSON describes the deployment's choices. Neither file alone necessarily represents the resolved settings. Keep this mapping explicit when adding or renaming settings.

Command-line overrides apply to a particular invocation. Document supported overrides and how they are exposed to discovery so persistent configuration is distinguishable from process-specific settings. Use JSON for lasting deployment changes.

Keep credentials and other secrets in separate protected files or the project's secret-management mechanism. BMGeoIP, for example, keeps database credentials in `/etc/bmgeoip/database.env`. The discoverable JSON must not require access to secrets.

## Preserve Configuration Through Deployment

Integrate configuration into [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}):

- On first installation, create the production JSON only when missing, using defaults from constants rather than a second hardcoded copy.
- Preserve existing files on reinstall and upgrade. Validate them against the incoming release before stopping services. Handle schema changes through explicit migrations that retain operator choices.
- Keep live JSON outside copied source artifacts and managed-file cleanup. Retain it on uninstall under the standard lifecycle contract unless the project documents another policy.
- Resolve settings once per process and document that edits require a restart. Provide a restart entry point that validates configuration before applying changes to all affected services and generated configuration.
- Run health checks with the same resolved settings as the application. Include configuration code, defaults, and operational consumers in [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) when enabled.

The starter installer does not supply an application runtime resolver or manage this JSON. Implement the project's configuration lifecycle before enabling its `DEPLOYMENT_READY` flag.

## Verify the Contract

Check missing and partial files, explicit overrides, invocation precedence, and changed release defaults. Verify malformed, unreadable, and invalid configuration fails before service changes. Confirm application consumers and operational tools resolve the same values.

Verify first installation, reinstall, upgrade, and uninstall preserve the intended configuration. After editing JSON and restarting, check effective application behavior and confirm CMDB reports the corresponding deployment settings. Keep configuration examples and the setting-to-constant mapping current as the schema evolves.

---

[Back]({{ site.baseurl }}{% link index.md %})
