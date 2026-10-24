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
| Bootstrapping an empty project with Codex skills | [Install pinned Codex component skills]({{ site.baseurl }}{% link pages/codex-skills.md %}) |
| Implementing or improving a component | [Component blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) and [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) |
| Building the DAL or classifying application code | [Activity / Interface / Entity]({{ site.baseurl }}{% link pages/classification.md %}) and [DB Server]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Centralizing constants and avoiding magic strings | [Constants standard]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Localizing application interfaces from day one | [Application Localization]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Selecting charts, maps or relationship graphs | [Approved display visualizations]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Configuring a service | [Runtime configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %}) and [network configuration]({{ site.baseurl }}{% link pages/network-configuration.md %}) |
| Integrating an installed application with CMDB | [CMDB compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Making an application monitorable | [Application health checks]({{ site.baseurl }}{% link pages/health-checks.md %}) |
| Installing, upgrading or uninstalling | [Installation Lifecycle contract]({{ site.baseurl }}{% link pages/component-installation.md %}), [installation scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) and [deployment impact]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Publishing a release | [Release setup]({{ site.baseurl }}{% link pages/release-setup.md %}), [creating a release]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [changelog maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) |
| Publishing documentation | [Jekyll setup]({{ site.baseurl }}{% link pages/jekyll-setup.md %}), [GitHub Pages]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [multilingual documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |

## Codex skill packaging

Start from the [greenfield bootstrap skill]({{ site.baseurl }}{% link pages/codex-skills.md %}) to install the pinned **project, constants, localization and installation** baseline, plus only the other components the user requests, into a new application's `.agents/skills/`. The project gets its own `AGENTS.md` and **read-only update notices**, never automatic upgrades or application generation.

## Component specifications

Each contract specifies behaviour, a **fixed approved runtime-module inventory**, and acceptance checks. Codex adapts the **frozen local reference code** rather than choosing other frameworks. If the prescribed modules are insufficient, Codex must stop and ask for approval before changing the specification.

| Component | Stable ID | Contract |
| --- | --- | --- |
| HTTP display server | `bmforge.http-server` | [HTTP]({{ site.baseurl }}{% link pages/component-http.md %}) |
| ZeroMQ REQ/REP | `bmforge.zmq-server` | [ZeroMQ]({{ site.baseurl }}{% link pages/component-zmq.md %}) |
| DB Server | `bmforge.db-server` | [Canonical DbMgr and DAL layering]({{ site.baseurl }}{% link pages/component-db-server.md %}) |
| Git | `bmforge.git` | [Publish and Commit]({{ site.baseurl }}{% link pages/component-git.md %}) |
| Display visualizations | `bmforge.visualization` | [Plotly.js, Leaflet, Cytoscape.js]({{ site.baseurl }}{% link pages/component-visualization.md %}) |
| Constants | `bmforge.constants` | [Domain-grouped fixed values]({{ site.baseurl }}{% link pages/component-constants.md %}) |
| Application localization | `bmforge.localization` | [English source and multilingual runtime UI]({{ site.baseurl }}{% link pages/component-localization.md %}) |
| Installation lifecycle | `bmforge.installation` | [Install/upgrade/uninstall, versioned footprint and client/server roles]({{ site.baseurl }}{% link pages/component-installation.md %}) |

## Traceability and improvement

Implementing modules carry a small, statically readable component ID and specification version. The [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) defines how to identify a gap, improve a contract, add a regression case, and version the change. The [decision record]({{ site.baseurl }}{% link DECISIONS.md %}) captures choices and unresolved work.

**Current state:** the HTTP, ZeroMQ, DB Server, Git, and optional display-visualization contracts, canonical DB/Git templates, and pinned local examples are drafts awaiting validation in consuming applications. The visualization choices are grounded in pinned MyCount and CMDB code. Codex skill packaging is implemented; live consumer validation and CMDB scanning of component tags remain future work. Existing CMDB declarations for files, databases, and listeners remain separate from architectural component tracing.

---

[Changelog]({{ site.baseurl }}{% link CHANGELOG.md %}) · [BMForge repository](https://github.com/NadimGhaznavi/bmforge) 
