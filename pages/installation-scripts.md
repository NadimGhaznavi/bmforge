---
title: Installation Scripts
lang: en
locale: en-US
language_name: English
translation_key: bmforge-installation-scripts
---

Every project provides executable `scripts/install.sh`, `scripts/upgrade.sh`, and `scripts/uninstall.sh`. Establish these entry points during project setup and implement their project-specific work as the application takes shape.

## Define the Lifecycle

| Script | Responsibility |
| --- | --- |
| `install.sh` | Validate prerequisites, provision required resources, deploy the application, configure owned services and schedules, and verify the result |
| `upgrade.sh` | Update an existing installation while retaining configuration, credentials, and persistent data; apply required migrations and restart affected services |
| `uninstall.sh` | Stop and remove owned services and schedules and remove managed application files while retaining configuration, credentials, databases, and persistent data |

All three scripts support `--help` without privileges or changes. Validate arguments and prerequisites before modifying the host. Operations under `/opt/prod` require root. Run from a separate source checkout, regardless of the caller's working directory. Scripts report failures with a nonzero exit status and support a read-only `--check` where useful.

Keep shared deployment mechanics in one helper instead of duplicating them across the entry points. Reuse provisioning only when it is safe during upgrades. Document prerequisites, retained state, and any project-specific behavior in the project's installation guide.

## Start from the Templates

Copy the [install]({{ '/templates/project/scripts/install.sh' | relative_url }}), [upgrade]({{ '/templates/project/scripts/upgrade.sh' | relative_url }}), and [uninstall]({{ '/templates/project/scripts/uninstall.sh' | relative_url }}) entry points and their [Python helper]({{ '/templates/project/scripts/install.py' | relative_url }}) into the project's `scripts/` directory. Include the metadata checker from [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}).

```sh
chmod +x scripts/install.sh scripts/upgrade.sh scripts/uninstall.sh
```

The helper is a source-file deployment baseline. Replace its project name and package placeholders, define its managed file and directory lists, and implement any provisioning, service lifecycle, schema migration, and health checks the project needs. It starts with `DEPLOYMENT_READY = False` and refuses deployment until that work is ready. Stubbed steps must not report success.

For a source-only toolkit, the baseline can be sufficient once its file lists are configured. [BMForge's installation]({{ site.baseurl }}{% link pages/installing-bmforge.md %}) is an example. Applications with running services or databases need their own additional work before enabling deployment.

## Preserve Data and Deployment Identity

Deploy to the literal `BASE_DIR` and install readable constants at the path specified by [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}). Directory permissions must allow the inventory account to traverse the path and read the metadata. Credentials stay outside public source files.

Use explicit managed file lists or an ownership manifest. Keep persistent data and live configuration outside copied source trees. The baseline does not infer protected data paths from CMDB declarations; configure and test that separation explicitly. Refuse unexpected paths and symlinks, preserve unowned files, and remove only project-owned resources. Uninstallation is not a data purge.

The baseline records ownership in `.installation-manifest.json` and the last successful version in `.deployment-version`. When uninstallation retains unowned files, it leaves an empty ownership record so subsequent installation or removal can recognize the directory. Constants are copied after other managed files; the successful-version marker advances only when the operation completes. Individual files are replaced atomically, but the whole deployment is not transactional. An interrupted operation can leave mixed application files; report the failure and inspect or retry from the source checkout.

## Connect Releases and Verify

Release publication and host deployment are separate processes. Run installation or upgrades from the intended release checkout. The release script checks that the three lifecycle entry points are executable, have valid shell syntax, and are committed; it does not run them or certify their project-specific behavior.

For selective upgrades, include lifecycle scripts and their dependencies in [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}). Preserve the last successful version before replacing application files, execute the planned work, and publish success bookkeeping after health checks.

Verify first installation, reinstallation, upgrades, repeat uninstallation, retained configuration and data, removed obsolete files, readable CMDB metadata, invalid paths, and interrupted work. Run filesystem checks in temporary directories and service or database checks in an appropriate disposable environment. Verify a real CMDB scan after deployment.

---

[Back]({{ site.baseurl }}{% link index.md %})
