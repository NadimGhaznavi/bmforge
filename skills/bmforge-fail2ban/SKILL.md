---
name: bmforge-fail2ban
description: Connect application security logs to a host-local blocking service using Fail2ban filters, jails and a thin ZMQ action client. Use for detecting logged malicious activity and requesting timed bans. Requires bmforge-zmq; does not implement a log watcher or change firewall rules directly.
---

# Security logs to local ban requests

Read `references/specification.md` and `references/engineering-contract.md`. Require the project-local `bmforge-zmq` skill for its existing REQ/REP transport and envelope. Select both explicitly if ZMQ is absent.

- Keep applications responsible only for a trusted, single-line security event with timestamp, stable event name and numeric client IP. Use the established logging path; no application blocking client is required.
- Use native Fail2ban filters and jails for matching, `findtime`, `maxretry`, finite `bantime` and `ignoreip`. Do not write another log parser, watcher, scheduler or detection engine.
- Create one application-owned Fail2ban action and a thin command-line client for ban/unban requests to the blocking service on the same host. Pass only the validated address, configured jail/source and required ban timing; never pass raw matched log text to a shell.
- Reuse BMForge ZMQ REQ/REP, bounded waits and acknowledged results. Report a failed or uncertain operation with a nonzero client exit; do not silently retry or claim that a timeout means the ban was absent.
- Keep each source's ban independent: an unban from one jail must not release another jail's active ban. The blocking service owns this policy and enforcement; the action client never invokes nftables or firewalld.
- Add no centralized controller, general Fail2ban wrapper API, firewall backend selection, escalation engine, database or dashboard. Use upstream tools for their wider capabilities.
- Mark the owning client module with `BMFORGE_COMPONENT = {"id": "bmforge.fail2ban", "spec_version": "0.1.0"}`. Validate the filter with benign and malicious log fixtures, then exercise the local action path and failure cases from the specification.
