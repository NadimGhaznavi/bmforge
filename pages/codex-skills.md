---
title: Use BMForge with Codex
lang: en
locale: en-US
language_name: English
translation_key: bmforge-codex-skills
---

BMForge gives Codex a set of engineering skills for building new applications. **Install one entry-point skill**, then let Codex select and install the components your project needs.

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

---

[Back to BMForge]({{ site.baseurl }}{% link index.md %})
