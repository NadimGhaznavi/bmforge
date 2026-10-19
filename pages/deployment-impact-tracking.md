---
title: Deployment Impact Tracking
lang: en
locale: en-US
language_name: English
translation_key: bmforge-deployment-impact-tracking
---

Record which deployment targets each release changes, so upgrades can update affected components and combine changes across skipped releases. This optional tooling is adapted from MyCount's portable `deployment_tools` package. Configure it before enabling its hooks in [Release Setup]({{ site.baseurl }}{% link pages/release-setup.md %}).

## Copy the Tools and Project Policy

From a BMForge checkout, copy `templates/deployment_tools/` to the new project's `deployment_tools/` directory and `templates/project/deployment/` to its `deployment/` directory. Copy Python source files, including `__init__.py` and `__main__.py`, without caches or compiled bytecode. The source is also available in the [BMForge template directory](https://github.com/NadimGhaznavi/bmforge/tree/main/templates).

Replace `__PROJECT_NAME__` and `__PROJECT_SLUG__` in `deployment/config.py` and `deployment/rules.json`. Keep these names consistent with [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}).

| File | Responsibility |
| --- | --- |
| `deployment/rules.json` | Scanned files, dependency rules, and deployment target entry points |
| `deployment/DependencyMap.py.in` | Format of the generated dependency map |
| `deployment/DependencyMap.py` | Generated static target and dependency mappings |
| `deployment/config.py` | Version path, history path, scan roots, copy roots, and full-setup target |
| `deployment/releases.json` | Release history and the current artifact hashes and target ownership |

The starter has `application` and `filesystem` targets. Replace its `__main__.py` entry point with the actual application entry point, or retain it if the project runs as a Python module. Adapt targets to actual processes and services. MyCount uses `listener`, `report-server`, and `filesystem`; those are project-specific names.

The starter includes the lifecycle scripts and their shared helper from [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}). Extend the rules with service units, requirements, assets, schemas, and other deployment inputs as they are introduced. The starter is a minimal map, not a complete installer. Extend `scan_roots`, `package_roots`, and `setup_files` in the configuration to match what the installer manages. The policy module exposes a `DeploymentConfig` named `CONFIG` and imports the generated map; it is ordinary trusted project code.

## Generate and Check Dependencies

Run from the project root:

```sh
python3 -B -m deployment_tools --rules deployment/rules.json
python3 -B -m deployment_tools --rules deployment/rules.json --check
```

The generator scans local Python imports, Python heredocs in shell scripts, and static template references. Declare shell calls, dynamic references, and dependencies it cannot infer under `extra`. Every scanned artifact must be reachable from a target. Missing dependencies, cycles, and unowned files fail generation.

Commit the generated map. `--check` compares it with the rules without modifying it; use that check before releases. Declare template roots when scanning templates. Keep the changing release manifest outside the artifact map so it does not hash itself.

## Initialize Release History

After configuring the map, initialize a baseline matching the current literal `VERSION`:

```sh
python3 -B -m deployment_tools.release --config deployment.config initialize 0.0.0
```

Commit `deployment/releases.json` with the configuration and generated map. Initialization refuses to overwrite existing history. Establish the baseline before making the changes intended for the next release; initializing afterward would treat those changes as already present. For an existing deployed project, establish a baseline from a known release and account for older installed versions before enabling selective upgrades.

Set both release-script settings:

```sh
readonly dependency_rules="deployment/rules.json"
readonly deployment_config="deployment.config"
```

The release script checks the map and baseline before merging, checks again on `dev`, then prepares and commits the new history after updating the release constants. Artifact additions, changes, deletions, and ownership changes determine affected targets. Only the automatic `VERSION` edit is excluded from hashing; codename and other constants changes retain their declared impact.

## Select Upgrade Work

The installer owns service stops, copying, dependency installation, schema changes, service starts, and health checks. Use `ReleaseFiles`, `ReleaseDeployment`, and `DeploymentFiles` from `deployment_tools` with `deployment.config.CONFIG` to select and apply its work.

To inspect targets for an upgrade from a known installed version:

```sh
python3 -B -m deployment_tools.release --config deployment.config upgrade 0.0.0 0.1.0
```

Target names are printed one per line. The planner combines all intervening releases; a full-setup target expands the result to every target. Unknown installed versions, a mismatched checkout version, and artifacts changed since release preparation fail instead of guessing.

Read the installed version with `ReleaseFiles.installed_version()`. Preserve the last successful version in `.deployment-version` before replacing application files. `DeploymentFiles.copy_application()` copies selected package files and removes obsolete managed package files; `copy_setup()` copies the configured setup files. Call `complete(version)` only after the selected deployment and health checks succeed to publish release bookkeeping. These copy helpers do not provide a transactional rollback of application files.

Test the project's actual installer independently. Selective deployment is ready only when it handles affected services, skipped releases, failed upgrades, removed files, and preserved configuration and data.

---

[Back]({{ site.baseurl }}{% link index.md %})
