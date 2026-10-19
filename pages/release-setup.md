---
title: Release Setup
lang: en
locale: en-US
language_name: English
translation_key: bmforge-release-setup
---

Prepare a new project's release tooling once. Use [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %}) for subsequent releases.

## Prepare the Constants and Changelog

Complete [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) first. Establish the canonical application name, constants path, literal `VERSION`, and initial `CMDB_CODENAME`.

Create `CHANGELOG.md` with exactly one `## [Unreleased]` heading. The [changelog template]({{ '/templates/project/CHANGELOG.md' | relative_url }}) provides the initial structure. Follow [Changelog Maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) to keep it current during development and maintenance.

## Install the Scripts

Copy these files from BMForge into the new project:

| BMForge source | Project destination |
| --- | --- |
| [Release script]({{ '/templates/project/scripts/new-release.sh' | relative_url }}) | `scripts/new-release.sh` |
| [Metadata checker]({{ '/templates/project/scripts/check-cmdb.py' | relative_url }}) | `scripts/check-cmdb.py` |

Make `scripts/new-release.sh` executable. It requires Bash, Git, Python 3.10 or newer, and standard GNU command-line tools. It reads and edits metadata without importing application code.

Replace `__PROJECT_NAME__` and `__PROJECT_SLUG__` in the script's settings block with the canonical application name and its lowercase form. Review the version path, changelog path, remote, and branch names. The standard defaults are `origin`, `dev`, `main`, and `feat/maint-`.

Deployment impact tracking is configured separately. Leave `dependency_rules` and `deployment_config` empty until [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) is ready; enable both together when using it.

## Establish the Branches

Start with a committed initial project on `main` and an `origin` remote. Create the development and first feature branches:

```sh
git switch main
git switch -c dev
git switch -c feat/maint-0.1.0
```

Use an existing `dev` branch when one is already present. Feature work branches from `dev`. Before each release, `main` must be an ancestor of `dev`, and `dev` an ancestor of the feature branch. Local `main` and `dev` must contain their remote counterparts. The script can create missing remote branches during its release push.

## Verify the Setup

- Run the metadata checker with the actual project name and constants path.
- Run `bash -n scripts/new-release.sh` and `scripts/new-release.sh --help`.
- Commit the scripts, constants, changelog, and any configured deployment metadata before releasing.
- Exercise an adapted release script in a disposable repository with a local bare remote. Verify matching version, codename, changelog, branch tips, and annotated tag.

---

[Back]({{ site.baseurl }}{% link index.md %})
