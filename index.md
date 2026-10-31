---
layout: home
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: bmforge-home
---

![BMForge Logo](/pages/images/bmforge.png)

# BMForge

**Build small. Fail visibly. Own the implementation.**

BMForge is an engineering contract for coding agents. It defines how applications are built, tested, released, and integrated with the local environment. It is **not a shared runtime library**: each application owns its code. Separate applications interact only through documented public APIs.

BMForge is another fine product from the [Bear & Moose](https://osoyalce.com) brand.

## Start with Codex

Install the **`bmforge` skill** once in a Codex chat:

```text
$skill-installer install https://github.com/NadimGhaznavi/bmforge/tree/main/skills/bmforge
```

Then invoke `$bmforge` in Codex. In a new repository, it bootstraps the engineering baseline and your chosen components. In an existing repository, it can attach just the selected skill, such as RCA, without changing the application architecture or release process. See the [short setup guide]({{ site.baseurl }}{% link pages/codex-skills.md %}).

## The engineering contract

Read the [engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %}) before implementing anything.

- **Lean by default:** build only what is required. Every abstraction, service, retry, and fallback needs a reason.
- **Trust contracts:** validate at external boundaries; don't revalidate trusted internal data at every layer.
- **Fail visibly:** broken internal assumptions, unavailable required resources, and unsuccessful operations must not look like success.
- **Respect distributed boundaries:** explicit acknowledgements and timeouts where delivery matters; no invented resiliency architecture.
- **Verify behaviour:** test the selected component contracts and meaningful failure paths, not imaginary requirements.
- **Expose health:** running applications provide a simple, on-demand health result for monitoring.

## Start a task

| What Codex is doing | Authoritative starting point |
| --- | --- |
| Building an application | Root `AGENTS.md`, [engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %}), [class classification]({{ site.baseurl }}{% link pages/classification.md %}), then selected [component blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) |
| Starting a new project with Codex | [Use BMForge with Codex]({{ site.baseurl }}{% link pages/codex-skills.md %}) |
| Implementing or improving a component | [Component blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) and [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) |
| Building the DAL or classifying application code | [Activity / Interface / Entity]({{ site.baseurl }}{% link pages/classification.md %}) and [DB Server]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Centralizing constants and avoiding magic strings | [Constants standard]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Localizing application interfaces from day one | [Application Localization]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Selecting charts, maps or relationship graphs | [Approved display visualizations]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Editing timeline objects | [Timeline Editing (requires HTTP)]({{ site.baseurl }}{% link pages/component-timeline.md %}) |
| Publishing an application security event without blocking dependencies | [Security Event Producer]({{ site.baseurl }}{% link pages/component-security-events.md %}): journald and trusted request context |
| Blocking malicious IPs on one host from security events | [Fail2ban journal detection]({{ site.baseurl }}{% link pages/component-fail2ban.md %}) and [nftables timed bans]({{ site.baseurl }}{% link pages/component-nftables.md %}) |
| Exporting rendered frames as an animated GIF | [GIF Animation]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Configuring a service | [Runtime configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %}) and [network configuration]({{ site.baseurl }}{% link pages/network-configuration.md %}) |
| Integrating an installed application with CMDB | [CMDB compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Making an application monitorable | [Application health checks]({{ site.baseurl }}{% link pages/health-checks.md %}) |
| Investigating a production defect | [RCA skill](https://github.com/NadimGhaznavi/bmforge/blob/main/skills/bmforge-rca/SKILL.md): collect evidence read-only and troubleshoot locally |
| Installing, upgrading or uninstalling | [Installation Lifecycle contract]({{ site.baseurl }}{% link pages/component-installation.md %}), [installation scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) and [deployment impact]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Publishing a release | [Release setup]({{ site.baseurl }}{% link pages/release-setup.md %}), [creating a release]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [changelog maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) |
| Creating or publishing a project website | [Project GitHub Pages standard]({{ site.baseurl }}{% link pages/jekyll-setup.md %}) (`bmforge-github-pages`), [publishing]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [multilingual documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |

## Component specifications

Each contract specifies behaviour, a **fixed approved runtime-module inventory**, and acceptance checks. Codex adapts the **frozen local reference code** rather than choosing other frameworks. If the prescribed modules are insufficient, Codex must stop and ask for approval before changing the specification.

| Component | Stable ID | Contract |
| --- | --- | --- |
| Project documentation site | `bmforge.github-pages` | [GitHub Pages scaffold and styling]({{ site.baseurl }}{% link pages/jekyll-setup.md %}) |
| HTTP display server | `bmforge.http-server` | [HTTP]({{ site.baseurl }}{% link pages/component-http.md %}) |
| ZeroMQ REQ/REP | `bmforge.zmq-server` | [ZeroMQ]({{ site.baseurl }}{% link pages/component-zmq.md %}) |
| Timed host IP bans | `bmforge.nftables` | [nftables timeout sets]({{ site.baseurl }}{% link pages/component-nftables.md %}) |
| Security-event production | `bmforge.security-events` | [Fire-and-forget journald event producer (no prerequisites)]({{ site.baseurl }}{% link pages/component-security-events.md %}) |
| Security-journal detection | `bmforge.fail2ban` | [Fail2ban journal filter and local ZMQ action (requires ZMQ)]({{ site.baseurl }}{% link pages/component-fail2ban.md %}) |
| DB Server | `bmforge.db-server` | [Canonical DbMgr and DAL layering]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Git | `bmforge.git` | [Publish and Commit]({{ site.baseurl }}{% link pages/component-git.md %}) |
| Display visualizations | `bmforge.visualization` | [Plotly.js, Leaflet, Cytoscape.js]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Timeline editing | `bmforge.timeline` | [vis-timeline (requires HTTP)]({{ site.baseurl }}{% link pages/component-timeline.md %}) |
| GIF animation | `bmforge.gif-animation` | [Pillow GIF frame encoder]({{ site.baseurl }}{% link pages/component-gif-animation.md %}) |
| Constants | `bmforge.constants` | [Domain-grouped fixed values]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Application localization | `bmforge.localization` | [English source and multilingual runtime UI]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Installation lifecycle | `bmforge.installation` | [Install/upgrade/uninstall, versioned footprint and client/server roles]({{ site.baseurl }}{% link pages/component-installation.md %}) |

## Traceability and improvement

Implementing modules carry a small, statically readable component ID and specification version. The [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) defines how to identify a gap, improve a contract, add a regression case, and version the change. The [decision record]({{ site.baseurl }}{% link DECISIONS.md %}) captures choices and unresolved work.

**Current state:** Pinned Codex skills, release scaffolding and read-only offline update checks are implemented, including the optional GIF Animation and production RCA skills. Component contracts and reference implementations remain drafts undergoing validation in consuming applications. CMDB scanning of component version markers is still planned.

---

[Changelog]({{ site.baseurl }}{% link CHANGELOG.md %}) · [BMForge repository](https://github.com/NadimGhaznavi/bmforge) 
