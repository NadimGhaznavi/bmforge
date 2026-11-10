---
title: ZeroMQ Request/Reply Component
lang: en
locale: en-US
language_name: English
component_id: "bmforge.zmq-server"
spec_version: "0.4.0"
spec_status: "draft"
translation_key: bmforge-component-zmq
---

**Component:** `{{ page.component_id }}` · **Contract:** `{{ page.spec_version }}` ({{ page.spec_status }}) · **Architecture view:** first draft

**Start here:** [Use cases](#use-cases) · [Analysis](#analysis-model) · [Design](#design-model) · [Code](#implementation-and-source) · [Traceability](#traceability)

This is the **human-facing map** of the ZeroMQ REQ/REP component. It shows what it does, what is responsible for what, and where to inspect the implementation. The [complete technical contract]({{ site.baseurl }}{% link pages/component-zmq-contract.md %}) remains authoritative for Codex, including the approved modules, TCP/IPC rules, error handling and acceptance checks.

## From behaviour to code

![Four-stage ZeroMQ traceability diagram: use cases lead to analysis responsibilities, proposed design classes and frozen source snapshots. The human reviews the design; Codex implements it.]({{ '/pages/images/zmq-architecture.svg' | relative_url }})

The **human approves the use cases and design**. Codex implements within that baseline. Code is inspectable but does not need line-by-line human approval. The class model below is **provisional**: it describes the existing contract and reference code, not an approved new implementation.

## Use cases

| ID | Actor and goal | Success / failure |
| --- | --- | --- |
| **UC-01** | Application client exchanges a command or query. | One versioned JSON request gets one correlated reply, within a bounded timeout. |
| **UC-02** | Application client sends invalid or unsupported input. | Structured error returned; the listener remains usable. |
| **UC-03** | Health probe checks the existing endpoint. | `health` returns `ok`, or a bounded failure when unavailable. |
| **UC-04** | Service owner starts, stops or reconfigures the listener. | Bind readiness and failures are visible; TCP or protected local IPC is selected; shutdown releases the socket. |

These are summaries, not replacement acceptance criteria. See [contract checks 1–10]({{ site.baseurl }}{% link pages/component-zmq-contract.md %}#acceptance-checks).

## Analysis model

**Problem-space responsibilities**, independent of Python classes:

| Role | Responsibility |
| --- | --- |
| **Boundary: Request/reply** | Accept one framed request and return one response; enforce the message/transport boundary. |
| **Entity: Message envelope** | Carry the protocol version, sender, target, method and payload. |
| **Control: Dispatch** | Route a validated request to an application-owned operation. |
| **Control: Lifecycle** | Establish readiness, report worker failure and stop cleanly. |

These are logical roles, not a requirement to create four Python classes. They follow BMForge's [Activity / Interface / Entity classification]({{ site.baseurl }}{% link pages/classification.md %}).

## Design model

**Solution-space classes**, subject to your design review:

| Design element | Responsibility and boundary | Reference |
| --- | --- | --- |
| **`ZMQServer`** (interface) | Own the REP socket and worker thread; poll, reply, signal readiness/failure and clean up. | [`ZMQServer.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/zmq/ZMQServer.py) |
| **`ZMQMsg`** (entity) | Serialize, parse and validate the versioned JSON envelope. | [`ZMQMsg.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/zmq/ZMQMsg.py) |
| **Application handler** (activity) | Interpret supported methods and perform application-specific work. **Outside** the reusable transport. | [`LookupHandler.py` example](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/server/LookupHandler.py) |
| **Application client** (interface) | Send a bounded REQ, receive the reply, and handle timed-out exchanges. | **Draft:** no pinned client snapshot yet. |

**Design decisions, not extra classes:** endpoint configuration selects TCP or a named IPC path; deployment owns IPC permissions and the single-server lifecycle. The application owns method names, authorisation and payload schemas. None of the draft names above expands the [approved runtime module inventory]({{ site.baseurl }}{% link pages/component-zmq-contract.md %}#approved-runtime-modules).

## Request/reply interaction

![Runtime sequence sketch: a client sends one REQ, the ZeroMQ worker parses the envelope, an application handler dispatches the command, and one REP returns a result or error.]({{ '/pages/images/zmq-exchange.svg' | relative_url }})

The same message contract applies to TCP and IPC. Malformed requests must receive an error instead of silently breaking the REP worker. A health probe uses the **same** endpoint, not an additional server.

## Implementation and source

This is a **frozen BMGeoIP reference snapshot**, not a full compliant implementation or a runtime BMForge dependency. Codex adapts the transport into each consuming application.

- [Socket worker: `ZMQServer.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/zmq/ZMQServer.py)
- [Message envelope: `ZMQMsg.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/zmq/ZMQMsg.py)
- [Application dispatch example: `LookupHandler.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/server/LookupHandler.py)
- [Protocol/timeouts example: `DZMQ.py`](https://github.com/NadimGhaznavi/bmforge/blob/main/components/reference/bmgeoip/bmgeoip/constants/DZMQ.py)
- [Codex component skill](https://github.com/NadimGhaznavi/bmforge/blob/main/skills/bmforge-zmq/SKILL.md)

The snapshot predates parts of contract `0.4.0`; it is **not evidence that every acceptance check passes**. Current consuming applications must supply and test any missing behaviour.

## Traceability

| Use case | Analysis responsibility | Design element | Verification |
| --- | --- | --- | --- |
| UC-01 | Boundary + envelope + dispatch | `ZMQServer`, `ZMQMsg`, handler, client | Checks 1, 6, 8 |
| UC-02 | Boundary + envelope | `ZMQMsg`, `ZMQServer` | Checks 2–4 |
| UC-03 | Boundary + dispatch | `ZMQServer`, app handler | Check 7 |
| UC-04 | Lifecycle + boundary | `ZMQServer`, app configuration | Checks 5, 6, 9, 10 |

[Open the full acceptance checks]({{ site.baseurl }}{% link pages/component-zmq-contract.md %}#acceptance-checks) · [Engineering contract]({{ site.baseurl }}{% link pages/engineering-contract.md %})

*Next iteration:* clickable class-level graph, contextual descriptions on selection, consuming-project code links and test-result links. This draft deliberately avoids adding a new viewer, framework or runtime dependency.

---

[Component catalogue]({{ site.baseurl }}{% link pages/technical-reference.md %}) · [Technical contract]({{ site.baseurl }}{% link pages/component-zmq-contract.md %})
