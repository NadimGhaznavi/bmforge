---
title: Fail2ban Security Log Detection
lang: en
locale: en-US
language_name: English
component_id: "bmforge.fail2ban"
spec_version: "0.1.0"
spec_status: "draft"
translation_key: bmforge-component-fail2ban
---

**Component ID:** `{{ page.component_id }}` · **Specification:** `{{ page.spec_version }}` ({{ page.spec_status }})

## Intent and prerequisite

Connect application security logs to a blocking service **on the same host**. Applications log malicious activity; native Fail2ban matches events and applies thresholds; a thin action client sends requests over [BMForge ZMQ REQ/REP]({{ site.baseurl }}{% link pages/component-zmq.md %}); the local service enforces bans through [nftables]({{ site.baseurl }}{% link pages/component-nftables.md %}). Each host operates independently. Follow the [engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %}).

**Requires `bmforge-zmq`.** Select both skills explicitly or use an already pinned ZMQ skill. The manager rejects a missing prerequisite before writing files. The enforcement project separately selects `bmforge-nftables`; installing this detection skill does not imply permission to modify its host firewall.

This contract covers only a security-event line, native filter/jail configuration and a ban/unban action client. Do not reproduce Fail2ban's log watcher, matching engine, scheduler, CLI or administration API. No centralized controller, escalation rules, new database, dashboard, direct firewall action or general backend abstraction is selected.

## Approved runtime modules

| Origin | Module/tool | Purpose |
| --- | --- | --- |
| Host package | `fail2ban`, `fail2ban-client`, `fail2ban-regex` | Native detection, jail configuration and verification |
| Python stdlib | `argparse`, `ipaddress`, `sys` | Thin client's argument parsing, numeric address validation and exit status |
| Existing component | `bmforge-zmq` approved modules, including `zmq` | Existing REQ/REP envelope, bounded exchange and acknowledged result |

Record the tested host package version in the application. Use native configuration files; do not import Fail2ban internals or introduce another Python wrapper library. Changes to this inventory require approval and a revised specification. Application policy and existing application logging remain outside the action client's module inventory.

## Application log boundary

Emit one trusted line containing a timestamp, a stable security-event name and the numeric client IP. For example:

```text
2026-10-30 20:00:00 SECURITY event=abuse ip=192.0.2.10
```

Use `yyyy-mm-dd hh:mm:ss` in the host/application local timezone, and configure Fail2ban to parse that same time policy. Reuse the application's logger and deployment log path; no special logging service is needed. The application determines which observed actions are malicious. Do not generate a security event for every ordinary validation error by default.

Build the line from fixed syntax, a server-selected event identifier and a validated address. Keep request paths, headers, usernames and other attacker-controlled free text outside the matched line, including newlines. Derive the client address from the connection or the explicitly trusted proxy chain, never an arbitrary forwarded header. An IP in a user-controlled message is not a ban target.

## Native filter and jail

Own one filter per required event pattern and a `.local` jail configuration. Leave vendor `.conf` files and unrelated jails unchanged. Configure only the required `logpath`, filter, `findtime`, `maxretry`, finite positive `bantime`, `ignoreip`, `usedns = no` and custom action. Choose values for the actual application; this skill supplies no universal ban threshold.

For the example line, after Fail2ban removes its recognized timestamp, an anchored filter can use:

```ini
[Definition]
failregex = ^\s*SECURITY event=abuse ip=<HOST>\s*$
ignoreregex =
```

Verify timestamp recognition with `fail2ban-regex`, not only with Python regex. Match only the selected fixed event name; benign lines and free-text imitations must not trigger it. IPv4 and IPv6 must both work. Configure protected administrative/proxy addresses through native `ignoreip` and the blocking service's existing policy as required by the host.

## Action client boundary

Use native `actionban` and `actionunban` to invoke a fixed, absolute application-owned executable. Pass the validated `<ip>`, a configured jail/source identifier and the effective ban timing required by the service's documented contract. Native `<bantime>` and `<time>` tags can supply the ban interval and ticket time; verify their behavior on the installed version, including restored tickets. Do not reset a restored ban to a fresh full interval.

The client converts these few arguments into the blocking service's declared ban/unban messages using the existing BMForge envelope. It has no log parsing, detection, policy or firewall code. Keep action parameters operator-controlled, restrict identifiers to a safe token alphabet and quote arguments; never interpolate `<matches>` or raw log text into a command.

Use the same-host loopback endpoint, never a wildcard bind or remote controller. Loopback is reachability, not caller authentication: the blocking service must authorize local callers under the application's declared local trust boundary. Do not invent a new authentication framework in this skill.

Return exit status zero only after a successful service acknowledgement of the requested result. A missing service, rejected request, timeout or error reply produces a visible diagnostic and nonzero exit. A lost reply leaves an uncertain outcome; do not blindly retry or extend a ban. Reuse the ZMQ contract's socket cleanup after a failed REQ exchange.

The blocking service owns effective expiry and independent source claims. Unbanning one jail releases only that source's request, preserving another active source. Natural kernel expiry and an already expired source must make later unban harmless. Stopping one jail must not flush a shared ban set. Fail2ban remains the detection/threshold engine; this contract adds no second expiry scheduler or persistent store.

## Traceability and references

Place `BMFORGE_COMPONENT = {"id": "bmforge.fail2ban", "spec_version": "0.1.0"}` in the action client's owning module, following [specification traceability]({{ site.baseurl }}{% link pages/specification-lifecycle.md %}). Follow the [installation lifecycle]({{ site.baseurl }}{% link pages/component-installation.md %}) for owned filters, jail/action files and executable; installing the skill itself never enables a jail or starts a service. This draft still requires validation in the standalone consuming project.

Consult upstream [jail/filter/action documentation](https://github.com/fail2ban/fail2ban/blob/master/man/jail.conf.5), [action configuration example](https://github.com/fail2ban/fail2ban/blob/master/config/action.d/dummy.conf) and [action ticket tags](https://github.com/fail2ban/fail2ban/blob/1.1.0/fail2ban/server/actions.py) for native details. They do not expand this contract's supported subset.

## Acceptance checks

1. Install/attach with ZMQ explicitly selected or already pinned; reject a missing prerequisite without file changes. Preserve the existing ZMQ bundle and lock entry when adding this skill.
2. Use `fail2ban-regex` on fixtures with valid IPv4/IPv6 events, benign lines, wrong event names, malformed addresses and injected/free-text imitations. Verify parsed timestamps and the configured local timezone.
3. In a disposable host, cross the configured threshold inside `findtime`; observe one native action reaching the local service and the resulting timed nftables ban. Below-threshold events and `ignoreip` entries must not cause bans.
4. Exercise ban and unban through a real local ZMQ exchange, with the declared source and timing. Two jails banning the same IP must survive either jail's unban/stop until the remaining claim ends.
5. Verify missing listener, error reply, rejected input and lost acknowledgement yield a nonzero client result and visible Fail2ban action failure, without direct firewall commands or hidden retries.
6. Reload/restart with active or restored tickets and verify remaining lifetimes are not reset. Verify natural kernel expiry makes subsequent unban harmless and removing this application's configuration preserves unrelated jails.

---

[Timed Host IP Bans]({{ site.baseurl }}{% link pages/component-nftables.md %}) · [Component Blueprints]({{ site.baseurl }}{% link pages/component-blueprints.md %})
