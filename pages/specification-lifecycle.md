---
title: Specification Lifecycle and Traceability
lang: en
locale: en-US
language_name: English
translation_key: bmforge-specification-lifecycle
---

# Specification Lifecycle and Traceability

BMForge defines the **current preferred contracts** for new implementations. Each application owns its implementation and may upgrade deliberately, without any runtime link to BMForge.

## Identify the implemented contract

Every BMForge-derived component must place one literal marker in its **owning Python module**, for example DevLog's ZeroMQ server:

```python
BMFORGE_COMPONENT = {
    "id": "bmforge.zmq-server",
    "spec_version": "0.1.0",
}
```

The stable ID identifies the BMForge component; the version identifies the specification used when the implementation was built or reviewed. It is **not** the application's release version. Tag the module that owns the component, not every helper file. The declaration must use literal strings so future discovery can parse it statically with Python AST, without importing or executing application code. No BMForge runtime import is required.

A marker is a **provenance claim**, not proof of compliance. Tests establish whether the implementation satisfies that contract.

## Evolving a specification

1. Investigate a failure in the consuming application. Distinguish an implementation defect from a missing or incorrect BMForge requirement.
2. For a specification gap, clarify the behaviour and add a focused acceptance or regression check.
3. Change the specification version when its required behaviour changes. Do not reuse a published version for a different contract. Preserve published versions as immutable Git-retrievable revisions or snapshots so old tags retain meaning.
4. Update the current specification page, its acceptance checks, and the [decision record]({{ site.baseurl }}{% link DECISIONS.md %}) when the change affects engineering policy or compatibility.
5. Consumers adopt the new version intentionally, test it locally, and update their own module markers.

Each component page declares its stable `component_id`, `spec_version`, and `spec_status` in page metadata. The three initial specifications are now **draft 0.2.0** contracts (including health checks) for DevLog validation, not yet published immutable releases.

## CMDB boundary and future visibility

A future CMDB application-code scanner can extract `BMFORGE_COMPONENT` markers and compare installed component versions with BMForge's catalogue. This will support both application-to-specification and specification-to-applications queries.

**This scanner and comparison report do not exist yet.** The existing `CMDB_COMPONENTS` declaration inventories persistent directories for backup and discovery; it must not be repurposed to mean BMForge architectural components.

An implementation that predates the latest specification is not automatically vulnerable or defective. Currency, tested compliance, and known security exposure are separate facts.

---

[Back to BMForge]({{ site.baseurl }}{% link index.md %})
