# OpenJS Foundation Security Update: May 2026

*Covering May 2026 | Powered by the Alpha-Omega Partnership*

May was a landmark month centered on the release of Node.js v26.0.0 — the last release under the traditional release model — alongside continued work on the Permission Model, security release automation, and LLM-assisted triage tooling.

## Node.js

### Node.js v26.0.0 Release

On **May 5, 2026**, Node.js v26.0.0 was officially released:

* [https://nodejs.org/en/blog/release/v26.0.0](https://nodejs.org/en/blog/release/v26.0.0)

This release was fully coordinated and delivered by RafaelGSS, covering changelog curation, release candidate validation, and cross-platform testing. Notable changes include:

* **Temporal API enabled by default** — the modern date/time API is now globally available without a flag, providing a robust alternative to the legacy `Date` object.
* **V8 updated to 14.6.202.33** (Chromium 146), introducing new JavaScript features:
  * `Map.prototype.getOrInsert()` and `WeakMap.prototype.getOrInsert()` / `getOrInsertComputed()`
  * `Iterator.concat()`
* **Undici 8.0.2** — updated HTTP client with new features and improvements.
* **Legacy stream modules removed** — `_stream_wrap`, `_stream_readable`, `_stream_writable`, `_stream_duplex`, `_stream_transform`, and `_stream_passthrough` have been removed.
* **`http.Server.prototype.writeHeader()`** removed in favor of `writeHead()`.
* Build toolchain requirements bumped: GCC 13.2 and Python 3.10+.

**Node.js v26 is the last release under the traditional release model.** Starting with Node.js v27, the project will adopt a new release cycle.

### Node.js Permission Model Improvements

Two significant improvements to the [Permission Model](https://nodejs.org/api/permissions.html) landed this month:

#### `permission.drop()` API

A new `permission.drop()` function was introduced, allowing applications to programmatically drop permissions at runtime:

* [https://github.com/nodejs/node/pull/62672](https://github.com/nodejs/node/pull/62672)

This enables a defense-in-depth approach where a process can relinquish access rights after the initialization phase is complete,
reducing the blast radius of exploitation.

Note that dropping a permission only removes future access grants and does not close existing file handles or sockets,
it is the application's responsibility to release those resources separately.

#### `--permission-audit` Flag Propagation Fix

A bug was fixed in which the `--permission-audit` flag was not properly handled when propagating flags to child processes and FFI calls:

* [https://github.com/nodejs/node/pull/63047](https://github.com/nodejs/node/pull/63047)

This ensures consistent permission auditing behavior across process boundaries.

### Automation of Security Release

#### HackerOne Report Template Update

The HackerOne security report template for Node.js was updated to include an explicit documentation review checklist, requiring reporters to confirm they have reviewed relevant API documentation, the Node.js threat model,
and common false-positive categories before submitting:

* [https://github.com/nodejs/TSC/issues/1856](https://github.com/nodejs/TSC/issues/1856)

This change directly addresses the growing volume of AI-generated or low-quality reports that do not account for documented behavior and threat model boundaries.

#### Improved H1 Report Validation in `node-core-utils`

A check was added to `node-core-utils` to detect HackerOne reports that are missing a `PR_URL`, improving the reliability of the automated triage pipeline:

* [https://github.com/nodejs/node-core-utils/pull/1074](https://github.com/nodejs/node-core-utils/pull/1074)

### LLM-Assisted H1 Report Triage

Work continues on a two-layer approach to assist the security team in triaging HackerOne reports:

* **Layer 1 — Rule-based classifier**: Filters noise by flagging reports with positive signals (PoC, repro steps, Node.js version) and deprioritizing known low-quality patterns (framework vulnerabilities, scanner output, app-level issues). No reports are auto-closed — only deprioritized for human review.
* **Layer 2 — LLM assessment**: Runs on reports that pass the classifier, using full context (past reports, threat model, relevant documentation) to produce a structured validity/severity assessment. The security team retains all decision authority.

Tracking issue: [https://github.com/nodejs/security-wg/issues/1554](https://github.com/nodejs/security-wg/issues/1554)

The tooling is being built directly into `node-core-utils` as `git node security --validate-reports`, with support for `codex`, `claude`, `copilot`, and custom LLM CLI backends. Successful assessments are cached locally to avoid redundant API calls:

* [https://github.com/nodejs/node-core-utils/pull/1079](https://github.com/nodejs/node-core-utils/pull/1079) _(work in progress)_

### ABI Stability on Semver Major Releases

An active TSC discussion was opened to reconsider the ABI stability constraints that have been blocking timely V8 updates in major releases:

* [https://github.com/nodejs/TSC/issues/1852](https://github.com/nodejs/TSC/issues/1852)

Node.js v26 was delayed to land V8 14.6, but that version was already outdated by the time the release shipped, with Chrome 148 (V8 14.8) having gone stable. The proposed change would allow ABI-breaking V8 updates to land during the Alpha and Current phases of a release, with the ABI frozen only when the release enters LTS:

> Starting with Node.js 27, Node.js may land V8 updates that require a native addon ABI version bump during the Alpha and Current phases. The native addon ABI is frozen when a release line enters LTS. N-API remains the recommended interface for native addons requiring ABI stability across Node.js versions.

The discussion is ongoing, with community and TSC input being gathered before formalizing the policy.

## Community

### GitHub Secure Open Source Meeting

Participated in the GitHub Secure Open Source meeting, engaging with the broader open source security community on best practices, tooling, and coordination across projects.
