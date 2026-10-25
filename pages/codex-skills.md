---
title: Codex Component Skills
lang: en
locale: en-US
language_name: English
translation_key: bmforge-codex-skills
---

# Codex Component Skills

BMForge's **user-level bootstrap skill** installs **project-local, pinned component skills** into a new Git repository. Codex discovers only the skills in the destination project, not the entire BMForge repository. Each installed skill includes its authoritative contract and the selected reference code. No application business logic or running service is generated. Bootstrap creates pinned skills and the established release-tooling scaffold.

## Install the bootstrap skill once

In Codex, use the built-in skill installer with:

```text
$skill-installer install https://github.com/NadimGhaznavi/bmforge/tree/main/skills/bmforge-new-project
```

Or, from a BMForge source checkout:

```sh
mkdir -p ~/.agents/skills
cp -R skills/bmforge-new-project ~/.agents/skills/
```

This **global** skill lives at `~/.agents/skills/bmforge-new-project/`. Use `$bmforge-new-project` in the destination Git repository. The skill asks which components the new application needs and does not assume a particular app or technology.

## Greenfield example

With Git already initialized in the destination repository, a user-approved selection such as HTTP and MariaDB can be installed with:

```sh
python3 ~/.agents/skills/bmforge-new-project/scripts/manage.py init \
    --project /path/to/new-repository \
    --name AcmeApp \
    --components bmforge-http,bmforge-db-server
```

Do **not** treat the example name or component choice as defaults. Required `--name` is a Python class name (e.g. `SnakeLab`), never a guessed repository slug; optional `--subtype` sets the CMDB subtype, default `Application`. Leaving `--components` out installs the four **baseline standards**: `bmforge-project`, `bmforge-constants`, `bmforge-localization` and `bmforge-installation`. They add instructions, English message catalogue examples and pinned templates, but generate no application code. Existing `AGENTS.md` or `.agents/` files are never overwritten.

The repository then has:

```text
AGENTS.md
CHANGELOG.md
acmeapp/
  constants/DAcmeApp.py
scripts/
  new-release.sh       # executable
  check-cmdb.py
  install.py           # deployment disabled
  install.sh           # executable
  upgrade.sh           # executable
  uninstall.sh         # executable
.agents/
  bmforge/
    manage.py
    lock.json
  skills/
    bmforge-project/
      SKILL.md
      references/
    bmforge-constants/
      SKILL.md
      assets/DProject.py
    bmforge-localization/
      SKILL.md
      assets/Localizer.py
      assets/DText.py
      assets/en.json
    bmforge-installation/
      SKILL.md
      references/specification.md
      references/source/devlog/
    bmforge-http/
      SKILL.md
      references/
    bmforge-db-server/
      SKILL.md
      references/
      assets/DbMgr.py
```

Each installed component's source commit, spec version and content fingerprint are recorded in `lock.json`. The original release templates are included in the pinned `bmforge-project` skill, so changes upstream are **reported as available**, never applied to generated project-owned release files. Components are available locally even if BMForge is later offline. There are **no runtime imports from BMForge**, and no ports, databases, application features or running services are created by installing skills. Release files are prepared **but never executed**. Once the application exists, the baseline [Installation Lifecycle skill]({{ site.baseurl }}{% link pages/component-installation.md %}) requires Codex to complete and test all three installation operations before the first release. Every successful installation records its version under the application-owned `/opt/prod` directory, even when installing only a custom library or CLI. Configure the app's deployment, Git origin and main/dev/feature branches, and commit the project before publishing a release. See [Release Setup]({{ site.baseurl }}{% link pages/release-setup.md %}).

## Available skills

| Project-local skill | Purpose |
| --- | --- |
| `bmforge-project` | Engineering policy; Activity / Interface / Entity classification (always installed) |
| `bmforge-constants` | Typed, domain-grouped constants; stable machine identifiers (always installed) |
| `bmforge-localization` | Request-scoped locale selection and English source catalogue (always installed) |
| `bmforge-installation` | Install/upgrade/uninstall completion, versioned `/opt/prod` identity and optional split client/server roles (always installed) |
| `bmforge-http` | Standard-library HTTP display server and optional Jinja2 |
| `bmforge-zmq` | PyZMQ REQ/REP server and message dispatch contract |
| `bmforge-db-server` | Unchanged canonical MariaDB `DbMgr.py` plus domain `*Db` interfaces |
| `bmforge-git` | Commit-all/push or managed-file publishing |
| `bmforge-visualization` | Plotly.js charts, Leaflet maps, Cytoscape.js topology graphs |
| `bmforge-gif-animation` | Pillow GIF frame encoding with controlled timing, palettes, looping, and bytes/file output |

**Existing projects:** Updating the global bootstrap skill or pinned project-local skills still requires explicit review and approval. The read-only checker will report available changes to the manager and skill bundles; it does not retrofit the new baseline into previously bootstrapped projects. A fresh bootstrap includes the new baseline automatically.

Add an optional component later, explicitly:

```sh
python3 .agents/bmforge/manage.py add --project . --components bmforge-zmq
```

The `add` operation refuses to replace an installed skill.

## Initialize the standard release branches

The **file-generation** step intentionally does not commit or push project files.
After reviewing the generated source, create/confirm the first commit on **local
`main`**. For a truly empty Git repository, initialize it explicitly with
`git init -b main` before BMForge bootstrap; otherwise work from an existing
local `main`, incorporating remote changes before setup.

Once the scaffold is committed and the working tree is clean:

```sh
python3 .agents/bmforge/manage.py setup-branches --project . --dry-run
python3 .agents/bmforge/manage.py setup-branches --project .
```

The first call is read-only; the second, only with the user's authorization,
creates **local** `dev` and `feat/maint-0.1.0` from `main` and checks out the
feature branch. The first feature name is configurable using
`--feature feat/maint-0.2.0`. No initial commit, Git push, remote branch,
merge, release, or tag is generated. It refuses partial/existing local or
remote-tracking refs, dirty repositories and a missing `main` commit rather
than assuming ownership of an existing history. Push local branches to
`origin` only with the user's separate approval.



## Update notification, not automatic upgrades

Use one **dedicated, clean local checkout** as the upstream snapshot for all projects.
This keeps the normal Codex session check offline, independent of GitHub access.
Create the cache once, outside Codex:

```sh
mkdir -p "$HOME/.cache"
git clone --single-branch --branch main \
    https://github.com/NadimGhaznavi/bmforge.git \
    "$HOME/.cache/bmforge-upstream"
```

Refresh it **separately**, when GitHub is accessible:

```sh
git -C "$HOME/.cache/bmforge-upstream" pull --ff-only
```

The checkout must remain clean and on `main`. Do not use a BMForge development
checkout with uncommitted edits as the update source. Set `BMFORGE_SOURCE` or pass
`--source /path/to/clean/bmforge` to use a different checkout.

The generated `AGENTS.md` asks Codex to run the **read-only, offline check**
before the first BMForge-derived coding change in a session:

```sh
python3 .agents/bmforge/manage.py check --project .
```

The check compares installed fingerprints to the cache's recorded Git commit.
It **does not** clone, fetch, pull or modify any checkout or application files.
A change to a skill or contract is reported even when the specification version
was not advanced; an unrelated BMForge commit does **not** create a false notice.

Possible results: `CURRENT`, `UPDATE AVAILABLE`, `LOCALLY MODIFIED`, and
`UPDATE CHECK UNAVAILABLE`. The reported local source commit identifies the
comparison point. **CURRENT means current relative to that cached commit, not
necessarily the newest GitHub commit.** A stale or unavailable cache cannot
establish whether new upstream updates exist. Refresh separately when appropriate.

`LOCALLY MODIFIED` is a separate integrity finding: the project's installed
skill differs from its lock even if the upstream cache is current. Inspect the
difference before any approved replacement. No updates are applied by the check.

**Nothing upgrades automatically.** Codex must tell the user what changed and
request authorization. The current tool intentionally has **no automatic upgrade
command**. An approved upgrade is a separate, reviewable step, preserving local
modifications and pinned provenance.

**Previously bootstrapped projects** retain their older pinned manager and
`AGENTS.md`. As an immediate workaround with the older manager, specify the
local checkout explicitly:

```sh
python3 .agents/bmforge/manage.py check --project . \
    --source "$HOME/.cache/bmforge-upstream"
```

Replacing the old manager/instructions remains a separately reviewed upgrade,
not something an update check performs.

## Verification

Use Python 3 and Git. To run the hermetic bootstrap tests from BMForge:

```sh
python3 -m unittest discover -s tests -p 'test_skill_bootstrap.py' -v
```

Tests create disposable local Git repositories, exercise selection, update notices, local modifications and refusal to overwrite; they do not build DevLog or make network requests.

---

[Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) · [Back to BMForge]({{ site.baseurl }}{% link index.md %})
