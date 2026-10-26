# BMForge

Engineering standards, component specifications and frozen reference implementations for Codex-driven projects. **No shared runtime code.**

## Use with Codex

In a Codex chat, install BMForge once:

```text
$skill-installer install https://github.com/NadimGhaznavi/bmforge/tree/main/skills/bmforge
```

Then open Codex in a **new Git repository** and invoke `$bmforge`. Codex will describe available skills and prepare the selected, pinned project-local components. See the [short setup guide](pages/codex-skills.md).

## Engineering references

- Start with [AGENTS.md](AGENTS.md) and the [engineering contract](pages/engineering-contract.md).
- Use [component blueprints](pages/component-blueprints.md), [class classification](pages/classification.md) and pinned local examples.
- Follow the [specification lifecycle](pages/specification-lifecycle.md) and [decision record](DECISIONS.md).
- Find component, installation, release and documentation contracts in [index.md](index.md).

Website: https://bmforge.osoyalce.com

The Codex skill packaging and read-only update checks are implemented. Component contracts continue to be validated in consuming applications; CMDB component scanning remains planned.
