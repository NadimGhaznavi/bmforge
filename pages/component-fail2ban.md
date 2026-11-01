---
title: Fail2ban Security Log Detection
lang: en
locale: en-US
language_name: English
component_id: "bmforge.fail2ban"
spec_version: "0.3.1"
spec_status: "draft"
translation_key: bmforge-component-fail2ban
---

**Component ID:** `{{ page.component_id }}` · **Specification:** `{{ page.spec_version }}` ({{ page.spec_status }})

## Intent and prerequisite

Consume an application's **systemd journal** security events on the same host. The independently selected [Security Event Producer]({{ site.baseurl }}{% link pages/component-security-events.md %}) emits one trusted record; **native Fail2ban** reads it from journald, optionally counts matches per address, and invokes a thin action client over [BMForge ZMQ REQ/REP]({{ site.baseurl }}{% link pages/component-zmq.md %}). The local service enforces bans through [nftables]({{ site.baseurl }}{% link pages/component-nftables.md %}). Each host operates independently. Follow the [engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %}).

**Requires `bmforge-zmq` in the blocking/consumer project** for its action client. Select both skills explicitly or use an already pinned ZMQ skill. The manager rejects a missing prerequisite before writing files. The event-producing application needs only `bmforge-security-events` and **must not** inherit this ZMQ dependency. The enforcement project separately selects `bmforge-nftables`; selecting this skill does not grant permission to modify the host firewall.

This contract covers only native journal-based filter/jail configuration and a ban-request action client; the event's format and trusted address are owned by the independent producer. The blocking service chooses the duration; the kernel holds the active block and expires it. Do not reproduce Fail2ban's log watcher, matching engine, scheduler, CLI or administration API. No centralized controller, escalation rules, new database, dashboard, direct firewall action or general backend abstraction is selected.

## Approved runtime modules

| Origin | Module/tool | Purpose |
| --- | --- | --- |
| Host package | `fail2ban`, `fail2ban-client`, `fail2ban-regex`, `python3-systemd` (or distribution equivalent), `systemd-journald` | Native journal backend, jail configuration and verification |
| Python stdlib | `argparse`, `ipaddress`, `sys` | Thin client's argument parsing, numeric address validation and exit status |
| Existing component | `bmforge-zmq` approved modules, including `zmq` | Existing REQ/REP envelope, bounded exchange and acknowledged result |

Record the tested host package version in the application. Use native configuration files; do not import Fail2ban internals or introduce another Python wrapper library. Changes to this inventory require approval and a revised specification. Application policy and existing application logging remain outside the action client's module inventory.

## Systemd journal event boundary

**Journald is the only supported delivery channel.** The independently selected [Security Event Producer]({{ site.baseurl }}{% link pages/component-security-events.md %}) writes exactly one line to a producing systemd service's existing stdout/stderr journal stream. Application business code only calls `emit("abuse")`; it never supplies an IP, counts events, retries delivery, saves ban state or knows the blocking service.

The canonical journal `MESSAGE` is **timestamp-free**:

```text
SECURITY event=abuse ip=192.0.2.10
```

Journald supplies the event time (e.g., `__REALTIME_TIMESTAMP`), hostname, service identity and PID as separate metadata. **Fail2ban's systemd backend reconstructs a prefixed line from `_HOSTNAME`, `SYSLOG_IDENTIFIER` (or `_COMM`), PID and `MESSAGE`.** Do not anchor the filter directly to `^SECURITY` against that full line, or expect Fail2ban to see `MESSAGE` alone. Use the native journal prefix pattern below. Never insert an additional timestamp, level, Gunicorn prefix or attacker-controlled free text inside the producer's `MESSAGE`.

Do not add a log file, `logpath`, rotation, independent watcher or fallback delivery backend. Verify the producing unit's `StandardOutput=journal` and `StandardError=journal`, and confirm the actual `_SYSTEMD_UNIT` recorded by the journal. Journal rate limits or service outages can lose events; fire-and-forget is **best effort**, not a guaranteed ban or an invitation to add an application queue.

## Native journal filter and jail

Use `backend = systemd` per jail, a real unit-scoped `journalmatch`, and the installed Fail2ban `common.conf` journal prefix pattern. The host's Fail2ban Python interpreter must have its native `systemd.journal` bindings; they are **not** a dependency in the producer's application venv.

A current Fail2ban 1.1.x filter for the exact canonical `abuse` event is:

```ini
[INCLUDES]
before = common.conf

[DEFAULT]
logtype = journal

[Definition]
failregex = ^%(__prefix_line)sSECURITY event=abuse ip=<HOST>$
ignoreregex =
journalmatch = _SYSTEMD_UNIT=myapp.service
```

`common.conf` already defines `__prefix_line` for journal mode, including the optional host and process/PID prefix. This uses Fail2ban's native format rather than a custom parser, date parser, or a catch-all `.*` prefix. Replace `myapp.service` and `abuse` with the actual trusted unit and selected event. Match only an allowlisted event name and numeric IPv4/IPv6 source. The special `<HOST>` capture must be parsed by Fail2ban with `usedns = no`. Test with **real** journal metadata and native `fail2ban-regex`; an offline representative prefix/regex fixture is useful, but is not proof of end-to-end journal matching.

Example disabled jail:

```ini
[myapp-abuse]
enabled = false
backend = systemd
filter = myapp-abuse
usedns = no
findtime = 60
maxretry = 1
bantime = 20h
ignoreip = 127.0.0.0/8 ::1
action = local-ban[source=myapp-abuse]
```

The native jail's `bantime` is a ticket/suppression interval, **not** the kernel ban duration. The blocking service chooses the duration. Leave `actionunban`, `actionstop` and `actionflush` empty; ticket expiry must not remove or shorten a kernel entry.

For **countable** events, create separate named filters/jails with identical journal matching but distinct fixed event identifiers. A disposable test may use `bad_request` (3 events in 60 seconds) and `auth_failure` (5 events in 300 seconds), each with its own `failregex`, `findtime`, and `maxretry`. Those are **test-only thresholds**, not recommended production settings. Fail2ban aggregates matches from all producing workers for the same trusted client address. The application must not maintain another counter or retry state. Confirm unrelated event names do not increment the other jail. When one IP independently crosses both thresholds, both jails may invoke the same ban-only action. Such repeated requests are permissible; do not add application cross-jail deduplication, source claims, or ban lifecycle tracking.

## Clean configuration ownership (no legacy migration)

New implementations ship only the **current** native arrangement. The consuming project's installer owns the explicitly declared `filter.d/<name>.conf`, `jail.d/<name>.conf`, and `action.d/<name>.conf` defaults. Operator-owned `*.local` overrides are separate and must not be overwritten. Native Fail2ban configuration layering supplies the effective settings; do not build a Python file merger, `configparser`-based translator or a legacy ownership-record compatibility engine.

During an authorized installation or upgrade, validate the **effective** native configuration, including any operator override. An override that switches a managed journal jail to `backend = auto`, restores `logpath`, widens `journalmatch`, enables an unverified jail or restores an unban hook **fails preflight**; never silently accept it. Retired project-owned native files must be removed by the application's explicitly reviewed deployment plan; unowned files remain untouched. For an older application, first **refactor its source, deployment rules, configuration and ownership records** to meet the current specification, then apply its normal release/deployment. BMForge does not provide compatibility transforms, fallback backends or automatic migration machinery.

The `bmforge-installation` contract owns the generic install/upgrade/uninstall ordering and preservation of unrelated operator data. This component owns only its current filter/jail/action file set, native preflight and activation checks.

## Native preflight and acceptance recipe

These checks establish **different facts**; passing one must not be reported as evidence of another. Perform on a disposable systemd host before enabling a production jail:

1. **Configuration structure:** verify each owned `.conf` file, operator `.local` precedence, effective `backend = systemd`, journalmatch, action hooks, and disabled-by-default jail. Run `fail2ban-client -t` for native parsing and `fail2ban-client -d` to inspect the effective command configuration. Neither proves a journal message matches.
2. **Host bindings:** inspect the installed `fail2ban.service` executable and check that **its interpreter**, not the producer's `.venv`, can `import systemd.journal`. E.g., on a host whose daemon uses OS Python, `/usr/bin/python3 -c 'import systemd.journal'`. Failure blocks activation; do not add this module to the application venv.
3. **Journal transport:** trigger a permitted test event from the **running application's normal request path**. Inspect `journalctl -u myapp.service -o cat` for the exact timestamp-free `MESSAGE`, and `journalctl -u myapp.service -o verbose` for actual `_SYSTEMD_UNIT`, event time, hostname, identifier and PID. Confirm the journal service is readable by Fail2ban's daemon account, not just an administrator.
4. **Actual matching:** run `fail2ban-regex -m '_SYSTEMD_UNIT=myapp.service' systemd-journal /etc/fail2ban/filter.d/myapp-abuse.conf`. Verify native journal timestamp handling, both IP families, exact event selection, and nonmatches for benign events, wrong unit, forged free text and misleading prefixes. Inspect matched and missed entries; do not substitute a synthetic plain logfile test.
5. **Independent counting:** on an isolated service/jail instance, emit below- and at-threshold sequences for **two** countable event names. Confirm each jail's own `findtime`/`maxretry` applies per address across workers; unrelated events do not cross-increment. With a controlled ban-action stub or isolated existing action, observe overlapping jails independently requesting bans for the same source only when their thresholds are crossed. Never send these fixtures to a live blocking service.
6. **Action boundary:** with the already-implemented local ZMQ client, verify successful native action dispatch and visible failure for an unavailable/rejecting service. Verify only `actionban` requests enforcement; stop, unban and ticket expiry do not. **Do not re-test nftables' already established core IP-blocking behavior** as a new integration prerequisite.

## Action client boundary

Use native `actionban` to invoke a fixed, absolute application-owned executable. Pass only the validated `<ip>` and a configured jail/source identifier for diagnostics. Do not send Fail2ban's ticket duration, deadline or an unban request. The blocking service chooses the effective duration from its own policy when inserting a new timed kernel entry.

Leave `actionunban`, `actionstop` and `actionflush` empty; do not inherit vendor firewall actions. Ticket expiry, manual jail unban and jail shutdown must leave enforcement untouched. Restored tickets may send another ordinary ban request; no special replay suppression is required.

The client converts these few arguments into the blocking service's declared ban request using the existing BMForge envelope. It has no log parsing, detection, policy or firewall code. Keep action parameters operator-controlled, restrict identifiers to a safe token alphabet and quote arguments; never interpolate `<matches>` or raw log text into a command.

Use the selected same-host ZMQ endpoint: a named filesystem IPC socket or explicitly configured loopback TCP, never a wildcard bind or remote controller. Apply the ZMQ contract's IPC permissions or the application's declared local authorization boundary; loopback reachability alone does not authenticate a caller. Do not invent a new authentication framework in this skill.

Return exit status zero only after a successful service acknowledgement of the requested result. A missing service, rejected request, timeout or error reply produces a visible diagnostic and nonzero exit. A lost reply leaves an uncertain outcome; do not blindly retry or extend a ban. Reuse the ZMQ contract's socket cleanup after a failed REQ exchange.

Keep the blocking service stateless between requests. The timed nftables entry is the sole live enforcement state; a jail/source identifier is diagnostic metadata, not an independent claim. Repeated requests after a restart are acceptable, including a fresh full duration; do not reconstruct old deadlines or track duplicates. Add no application ban map, source-claim ledger, expiry scheduler, persistence or recovery/replay subsystem. Fail2ban retains its own native detection state; the application does not mirror it. If kernel entries are lost, subsequent detection can request a new block.

## Traceability and references

Place `BMFORGE_COMPONENT = {"id": "bmforge.fail2ban", "spec_version": "0.3.1"}` in the action client's owning module, following [specification traceability]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}). Follow the [installation lifecycle]({{ site.baseurl }}{% link pages/component-installation.md %}) for owned filters, jail/action files and executable; installing the skill itself never enables a jail or starts a service. This draft still requires validation in the standalone consuming project.

The official [systemd-journald documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.html) describes how stdout/stderr records reach the journal. Fail2ban's native [jail.conf manual](https://github.com/fail2ban/fail2ban/blob/master/man/jail.conf.5) describes `backend = systemd`, `python3-systemd` and `journalmatch`. Verify the installed versions on the consuming host.

Consult upstream [jail/filter/action documentation](https://github.com/fail2ban/fail2ban/blob/master/man/jail.conf.5) and [action configuration example](https://github.com/fail2ban/fail2ban/blob/master/config/action.d/dummy.conf) for native details. They do not expand this contract's supported subset.

## Acceptance checks

1. A producer can install `bmforge-security-events` without HTTP, ZMQ, Fail2ban or nftables. Only the blocking/consumer project requires `bmforge-zmq` for `bmforge-fail2ban`; the manager rejects missing prerequisites before writing files.
2. Validate the journal-aware filter using Fail2ban 1.1.x `common.conf`, `logtype = journal`, `%(__prefix_line)s`, and the systemd backend's reconstructed hostname/identifier/PID prefix. A timestamp-free canonical `MESSAGE` from the producer must yield exactly the expected IPv4/IPv6 address; wrong service, event, prefix or injected text must never request a ban.
3. Preflight native configuration, daemon-interpreter `systemd.journal` support, real unit journal access and actual `fail2ban-regex` matches separately. Keep the jail disabled until the native checks pass. A syntactically valid filter file alone does not establish detection.
4. Preserve only the current spec's clean owned `.conf` defaults and separate operator `.local` overrides. Reject conflicting effective overrides; do not support automatic legacy migration, fallback file backends or historic ownership records. Refactor older consuming installations explicitly.
5. Exercise two countable event types with different native thresholds and both non-overlapping and overlapping per-IP failures. Each jail matches only its own event, and two independent thresholds can both invoke the same ban action. Never introduce producer-side counts, caches, IP state, retries or cross-jail deduplication.
6. Verify ban-only action behavior, missing service/error/timeout results and state-free restart. The kernel's existing timed bans are not revalidated in this journal integration.


---

[Timed Host IP Bans]({{ site.baseurl }}{% link pages/component-nftables.md %}) · [Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %})
