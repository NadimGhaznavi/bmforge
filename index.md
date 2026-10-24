---
layout: home
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: bmforge-home
---

![BMForge Logo](/pages/images/bmforge.png)

BMForge provides shared development standards, guidance, and reusable templates for coding agents creating new projects and working on existing projects.

Projects reference BMForge from their `AGENTS.md`. Project-specific instructions and exceptions stay in the project's own documentation.

## Objectives

- Formalize and extend the coding guidelines into a shared reference for agents
- Build a reusable software development toolkit for project setup, implementation, and maintenance
- Create a lightweight project management framework covering changelogs, releases, and documentation

## Guiding Principles

- Extract proven solutions from existing projects
- Add reusable templates as new solutions are developed
- Keep guidance clear and actionable for agents working across projects
- Give each document one clear purpose; link to related guidance instead of duplicating it

---

# Processes

- [Jekyll Setup]({{ site.baseurl }}{% link pages/jekyll-setup.md %})
- [GitHub Pages Publishing]({{ site.baseurl }}{% link pages/github-pages-publishing.md %})
- [Multilingual Documentation]({{ site.baseurl }}{% link pages/multilingual-documentation.md %})
- [CMDB Compliance]({{ site.baseurl }}{% link pages/cmdb-compliance.md %})
- [Runtime Configuration]({{ site.baseurl }}{% link pages/runtime-configuration.md %})
- [Network Configuration]({{ site.baseurl }}{% link pages/network-configuration.md %})
- [Installation Scripts]({{ site.baseurl }}{% link pages/installation-scripts.md %})
- Development and Maintenance
  - [Changelog Maintenance]({{ site.baseurl }}{% link pages/changelog-maintenance.md %})
- Release Management
  - [Initial Setup]({{ site.baseurl }}{% link pages/release-setup.md %})
  - [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %})
  - [Deployment Impact Tracking]({{ site.baseurl }}{% link pages/deployment-impact-tracking.md %})

---

## Components

- [Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %})
  - [HTTP Display Server]({{ site.baseurl }}{% link pages/component-http.md %})
  - [ZeroMQ Request/Reply Server]({{ site.baseurl }}{% link pages/component-zmq.md %})
  - [MariaDB Data Access]({{ site.baseurl }}{% link pages/component-database.md %})

---

## Using BMForge

[Install, Upgrade, and Uninstall]({{ site.baseurl }}{% link pages/installing-bmforge.md %})

[Changelog]({{ site.baseurl }}{% link CHANGELOG.md %})
