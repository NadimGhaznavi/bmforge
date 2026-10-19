---
title: Install, Upgrade, and Uninstall BMForge
lang: en
locale: en-US
language_name: English
translation_key: bmforge-installing-bmforge
---

BMForge deploys its source toolkit, documentation, and CMDB metadata under `/opt/prod/bmforge`. It has no application service, database, or scheduled job to provision. The documentation website is published separately through [GitHub Pages]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}).

## Prepare the Checkout

Use Linux with Bash and Python 3.10 or newer. Run from a separate BMForge checkout containing the intended release, such as `/opt/dev/bmforge`. The scripts locate that checkout themselves and can be invoked from another working directory. Review the release and keep local changes separate from the version being deployed.

Inspect help or validate file deployment without making changes:

```sh
scripts/install.sh --help
scripts/install.sh --check
```

An existing `/opt/prod/bmforge` without an ownership manifest is not automatically adopted. Inspect and reconcile that directory before installing.

## Install or Upgrade

For the first installation:

```sh
sudo scripts/install.sh
```

For an existing installation:

```sh
scripts/upgrade.sh --check
sudo scripts/upgrade.sh
```

Installation can be repeated. Upgrade requires an existing managed installation. Both copy the `bmforge/`, `scripts/`, `templates/`, and `pages/` source trees plus the root index, README, changelog, license, Jekyll configuration, and domain file. Git history, tests, caches, and compiled bytecode are not deployed. Obsolete managed files are removed; unowned files are retained. A new source file that would overwrite an unowned destination is rejected.

The installed constants are `/opt/prod/bmforge/bmforge/constants/DBMForge.py`. Verify them with:

```sh
python3 -B scripts/check-cmdb.py --name BMForge --root /opt/prod/bmforge bmforge/constants/DBMForge.py
```

Register `BMForge` in CMDB and scan applications to verify discovery. The local checker alone does not establish remote inventory access.

## Uninstall

From the separate source checkout:

```sh
scripts/uninstall.sh --check
sudo scripts/uninstall.sh
```

Uninstallation removes the manifest's managed files and successful-version marker, then removes empty managed directories. Unowned files and directories are retained, along with an empty ownership record when retained state remains. This allows repeated removal and later reinstallation without adopting an unrelated directory. The source checkout and hosted GitHub Pages site are unaffected; this command removes only the local installation.

If deployment fails, the script reports an error. It does not roll back files already copied. Inspect the installation before retrying; the ownership manifest accounts for partial copies, and `.deployment-version` records the last completed deployment when one exists.

---

[Back]({{ site.baseurl }}{% link index.md %})
