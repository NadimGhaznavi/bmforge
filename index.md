---
layout: home
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: bmforge-home
---

![BMForge Logo](/pages/images/bmforge.png)

BMForge is a **standalone software development toolkit for coding agents**. It collects proven engineering standards, component specifications, pinned reference implementations, and project setup/deployment tools so that new applications can be built quickly and consistently.

**BMForge is not a shared runtime library.** Every application owns its code and can evolve independently. Applications integrate with one another only through explicitly documented public APIs. Reference code is stored **inside BMForge** and copied/adapted into the consuming project, never imported from another project's repository.

## Start here: task-to-resource guide

| Your task | Start with | Then use |
| --- | --- | --- |
| Build an application from known components | [Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) | The selected component specifications and local reference code |
| Set up a new Python project or maintain an installation | [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %}) | [Runtime Configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %}), [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %}) |
| Add a listener or configure service endpoints | [Network Configuration]({{ site.baseurl }}{% link pages/network-configuration.md %}) | The relevant HTTP or ZeroMQ component specification |
| Create or publish a release | [Release Setup]({{ site.baseurl }}{% link pages/release-setup.md %}) | [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %}), [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %}) |
| Publish a website or documentation | [Jekyll Setup]({{ site.baseurl }}{% link pages/jekyll-setup.md %}) | [GitHub Pages Publishing]({{ site.baseurl }}{% link pages/github-pages-publishing.md %}), [Multilingual Documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %}) |
| Maintain project history | [Changelog Maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %}) | [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %}) |

## Components

These are **specifications for creating application-owned components**, with local examples and acceptance checks, rather than installed or shared packages.

| Component | Specification | Local reference |
| --- | --- | --- |
| HTTP Display Server | [HTTP Server]({{ site.baseurl }}{% link pages/component-http.md %}) | `components/reference/bmgeoip/bmgeoip/server/` |
| ZeroMQ REQ/REP Server | [ZeroMQ Server]({{ site.baseurl }}{% link pages/component-zmq.md %}) | `components/reference/bmgeoip/bmgeoip/zmq/` |
| MariaDB Data Access | [Database Access]({{ site.baseurl }}{% link pages/component-database.md %}) | `components/reference/bmgeoip/bmgeoip/interface/` |

Read [Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %}) first for the agent workflow, architectural boundaries, snapshot provenance, and definition of done. Each component page defines its own required behaviour and acceptance tests.

## Project standards and processes

**Project configuration and operations**

- [Runtime Configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %})
- [Network Configuration]({{ site.baseurl }}{% link pages/network-configuration.md %})
- [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %})
- [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %})
- [Install, Upgrade, and Uninstall BMForge]({{ site.baseurl }}{% link pages/installing-bmforge.md %})

**Release and maintenance**

- [Release Setup]({{ site.baseurl }}{% link pages/release-setup.md %})
- [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %})
- [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %})
- [Changelog Maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %})

**Websites and documentation**

- [Jekyll Setup]({{ site.baseurl }}{% link pages/jekyll-setup.md %})
- [GitHub Pages Publishing]({{ site.baseurl }}{% link pages/github-pages-publishing.md %})
- [Multilingual Documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %})

## Guidance for Codex

1. Read the repository's [`AGENTS.md`](https://github.com/NadimGhaznavi/bmforge/blob/feature/component-blueprints/AGENTS.md) and the resource matched to the requested task above.
2. Read only the relevant detailed specifications and their **local** reference code. Do not fetch moving upstream examples or introduce cross-project runtime imports.
3. Follow existing configuration, CMDB, installation, and release rules instead of inventing alternative conventions.
4. Implement in the consuming project's own namespace and test against the component's acceptance checks.
5. Keep project-specific exceptions and requirements in that project's own documentation. Request clarification before materially expanding scope.

## Current scope

BMForge currently covers **project setup and deployment**, **network and runtime configuration**, **CMDB discovery**, **releases and changelogs**, **Jekyll-based publishing**, **multilingual documentation**, and the three initial **HTTP, ZeroMQ, and MariaDB component blueprints**.

The component blueprints are being introduced together as the first specification-driven building blocks. Their practical completeness will be assessed when an independent application implements them. BMForge's reference files are examples for adaptation, not an executable standalone service.

---

[Changelog]({{ site.baseurl }}{% link CHANGELOG.md %}) · [BMForge repository](https://github.com/NadimGhaznavi/bmforge)
