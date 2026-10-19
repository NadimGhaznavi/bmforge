---
title: Changelog Maintenance
lang: en
locale: en-US
language_name: English
translation_key: bmforge-changelog-maintenance
---

Update `CHANGELOG.md` as part of everyday feature development, bug fixes, maintenance, and documentation work. Record meaningful outcomes as the work is completed, while its purpose and effects are clear.

## Where This Fits

| Stage | Responsibility | Process |
| --- | --- | --- |
| Project setup | Create the changelog and its `Unreleased` heading | [Release Setup]({{ site.baseurl }}{% link pages/release-setup.md %}) |
| Development and maintenance | Record completed changes under `Unreleased` | This process |
| Release | Assign the version and timestamp through the release script | [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %}) |

## Record the Change

1. Review the completed work and identify what changes for users, operators, or developers maintaining the project.
2. Add or update a concise entry beneath the existing `## [Unreleased]` heading. Keep exactly one such heading, spelled as shown.
3. Consolidate related details into a clear outcome. Use headings such as `Added`, `Changed`, `Fixed`, or `Removed` when they help organize the entries; omit empty sections.
4. Include the changelog update with the related changes when committing the work.

Describe implemented behavior and its practical effect. Include meaningful installation, configuration, compatibility, reliability, and documentation changes. Avoid a list of every edited file, intermediate attempts, or routine changes that have no meaningful effect on the project.

## Summarize Larger Changes

When a task involves many low-level changes, add or update `### Summary` directly below `## [Unreleased]`. Explain the problem and solution in one or two sentences. Keep supporting bullets only where they add useful detail, and retain entries for other unreleased work.

```markdown
## [Unreleased]

### Summary

The event log flickered during refresh. It now keeps existing entries visible as new events arrive.

### Fixed

- Preserve the selected event and scroll position during refresh.
```

## Hand Off to the Release Script

Leave released entries in place and record new work under `Unreleased`. During normal development, leave version numbers, release timestamps, and release codenames to the release process.

The release script inserts a versioned, timestamped heading immediately below `## [Unreleased]`. The accumulated entries become part of that release, and `Unreleased` remains empty and ready for the next changes. Follow [Creating a Release]({{ site.baseurl }}{% link pages/creating-a-release.md %}) when the work is ready to publish.

Before finishing a task, check that its changelog entry matches the actual result, related entries are consolidated, and the existing unreleased work and release history are preserved.

---

[Back]({{ site.baseurl }}{% link index.md %})
