---
title: Use BMForge with Codex
lang: en
locale: en-US
language_name: English
translation_key: bmforge-codex-skills
---

BMForge gives Codex selectable engineering skills for new and existing applications. **Install one entry-point skill** and select only the capabilities your project needs.

## 1. Install BMForge once

In a **Codex chat**, enter:

```text
$skill-installer install https://github.com/NadimGhaznavi/bmforge/tree/main/skills/bmforge
```

## 2. Start a new project

Open Codex in a **new Git repository** and enter:

```text
$bmforge
```

Codex will explain the available skills, ask for your application name and required components, and prepare the project. You do not need to manage individual skill installations or run setup scripts yourself.

The `bmforge` entry point lives in `~/.agents/skills/bmforge/`; selected component skills are copied into each project's `.agents/skills/` directory and pinned to a BMForge source revision. **No application is generated or deployed**, and updates require your approval.

## 3. Add a skill to an existing project

Open Codex in an established Git repository and enter `$bmforge`. Choose only the skill you need, such as `bmforge-rca` for read-only production evidence collection and local bug investigation. After you authorize the setup, Codex attaches that skill with its pinned version and local update checker.

**Existing projects retain their own `AGENTS.md`, architecture, application files, branches and release tooling.** Attachment does not install the new-project baseline or create a release scaffold. More skills can be added later with approval; checking for newer skills never upgrades them automatically.

For a project website, select **`bmforge-github-pages`**. It pins the
[GitHub Pages standard]({{ site.baseurl }}{% link pages/jekyll-setup.md %}),
configuration, Markdown templates and publishing workflow. The standard uses
the shared dark theme and requires the project's own logo. Applying the
templates is a separate implementation step; existing site content and
translations are preserved. This skill does not require the application HTTP
or Git components.

---

[Back to BMForge]({{ site.baseurl }}{% link index.md %})
