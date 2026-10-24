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
| Building an application | Root `AGENTS.md`, [engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %}), then selected [component blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) |
| Implementing or improving a component | [Component blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) and [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) |
| Configuring a service | [Runtime configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %}) and [network configuration]({{ site.baseurl }}{% link pages/network-configuration.md %}) |
| Integrating an installed application with CMDB | [CMDB compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Making an application monitorable | [Application health checks]({{ site.baseurl }}{% link pages/health-checks.md %}) |
| Installing or upgrading | [Installation scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) and [deployment impact]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Publishing a release | [Release setup]({{ site.baseurl }}{% link pages/release-setup.md %}), [creating a release]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [changelog maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) |
| Publishing documentation | [Jekyll setup]({{ site.baseurl }}{% link pages/jekyll-setup.md %}), [GitHub Pages]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [multilingual documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |

## Component specifications

Each contract specifies behaviour, a **fixed approved runtime-module inventory**, and acceptance checks. Codex adapts the **frozen local reference code** rather than choosing other frameworks. If the prescribed modules are insufficient, Codex must stop and ask for approval before changing the specification.

| Component | Stable ID | Contract |
| --- | --- | --- |
| HTTP display server | `bmforge.http-server` | [HTTP]({{ site.baseurl }}{% link pages/component-http.md %}) |
| ZeroMQ REQ/REP | `bmforge.zmq-server` | [ZeroMQ]({{ site.baseurl }}{% link pages/component-zmq.md %}) |
| DB Server | `bmforge.db-server` | [Specification]({{ site.baseurl }}{% link pages/component-db-server.md %}) |

## Traceability and improvement

Implementing modules carry a small, statically readable component ID and specification version. The [specification lifecycle]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}) defines how to identify a gap, improve a contract, add a regression case, and version the change. The [decision record]({{ site.baseurl }}{% link DECISIONS.md %}) captures choices and unresolved work.

**Current state:** the three contracts and locally pinned bmgeoip examples are a first draft awaiting validation in DevLog. Native Codex skill packaging and CMDB scanning of component tags are **planned, not implemented**. Existing CMDB declarations for files, databases, and listeners remain separate from architectural component tracing.

---

[Changelog]({{ site.baseurl }}{% link CHANGELOG.md %}) · [BMForge repository](https://github.com/NadimGhaznavi/bmforge) · [Component work in PR #1](https://github.com/NadimGhaznavi/bmforge/pull/1)
