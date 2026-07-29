# OpenJS Foundation Security Update: July 2026

*Covering July 2026 | Powered by the Alpha-Omega Partnership*

July focused on operationalizing the next generation of the Node.js security
release process. The main effort was the creation and use of a local security
release web viewer, supported by updates in `node-core-utils`, to manage the
July Node.js security release across report review, release-line readiness,
dependency updates, CVE requests, CI validation, and release communications.

## Node.js

### Node.js July 2026 Security Release

The Node.js project published a pre-release security announcement for the 26.x,
24.x, and 22.x release lines:

* [https://nodejs.org/en/blog/vulnerability/july-2026-security-releases](https://nodejs.org/en/blog/vulnerability/july-2026-security-releases)

The announcement states that the highest severity issue addressed by the release
is **High**. The security release was actively coordinated during the last week
of July, including release proposals for the active release lines, validation of
private fix and backport PRs, CI lockdown/release-day coordination, and release
communication preparation.

The original target date was Monday, July 27, 2026. A follow-up website update
was prepared to move the target to Tuesday, July 28, 2026, allowing additional
testing and validation before publication:

* [https://github.com/nodejs/nodejs.org/pull/9022](https://github.com/nodejs/nodejs.org/pull/9022)

The pre-release announcement PR was merged earlier in the month:

* [https://github.com/nodejs/nodejs.org/pull/9017](https://github.com/nodejs/nodejs.org/pull/9017)

### Security Release Web Viewer

A new local web viewer was created in the private `security-release` repository
to support day-to-day security release handling. The viewer is run locally with:

```sh
npm run dev
```

The viewer turns the active `vulnerabilities.json` file into an operations
dashboard for security release stewards. It provides:

* A release overview showing readiness, blockers, release phase, report counts,
  and next actions.
* Report operations views for HackerOne report metadata, severity, CVSS, team
  summaries, reporter and patch author metadata, affected release lines, and
  release readiness state.
* Release-line tracking for fix and backport coverage across `main`, 26.x,
  24.x, and 22.x.
* Dependency update tracking, including per-release-line PR coverage.
* GitHub and Jenkins validation views for release PRs.
* A final release checklist for publication tasks.
* A standalone threat-model assessment route for evaluating report text without
  adding it to the active release file.
* Local-only `admin.local.json` sidecars for private operational state, keeping
  committed `vulnerabilities.json` files focused on public release metadata.

Two notable security-release repository changes landed to support this workflow:

* Added the ability to start a new security release from the viewer and added
  the standalone `/assess` route for threat-model evaluation.
* Added a backport cleanliness command and viewer integration so release
  stewards can check whether backports contain only the expected security
  release commits before proceeding.

### `node-core-utils` Support for the Web Viewer

Several `node-core-utils` changes landed so the CLI release automation can work
with the web viewer's updated release metadata model:

* [nodejs/node-core-utils#1110](https://github.com/nodejs/node-core-utils/pull/1110) - Improved `git node security --start` UX by offering Tuesday release date choices.
* [nodejs/node-core-utils#1111](https://github.com/nodejs/node-core-utils/pull/1111) - Added an include-all report selection mode, making the CLI better suited for web-viewer-driven report review.
* [nodejs/node-core-utils#1112](https://github.com/nodejs/node-core-utils/pull/1112) - Cleaned up dependency update formatting.
* [nodejs/node-core-utils#1118](https://github.com/nodejs/node-core-utils/pull/1118) - Added support for `affectedVersions` as an object, matching the viewer's per-release-line PR map.
* [nodejs/node-core-utils#1119](https://github.com/nodejs/node-core-utils/pull/1119) - Added announcement references to the top-level vulnerability JSON.
* [nodejs/node-core-utils#1120](https://github.com/nodejs/node-core-utils/pull/1120) - Improved the developer experience of CVE requests during release preparation.
* [nodejs/node-core-utils#1122](https://github.com/nodejs/node-core-utils/pull/1122) - Updated post-release automation to handle object-shaped `affectedVersions`.
* [nodejs/node-core-utils#1124](https://github.com/nodejs/node-core-utils/pull/1124) - Changed `git node release --prepare --security` to select security release PRs from the `affectedVersions` map, including dependency updates and release-line-specific PRs.
* [nodejs/node-core-utils#1125](https://github.com/nodejs/node-core-utils/pull/1125) - Fixed cherry-pick message generation by reusing the amended message helper.
* [nodejs/node-core-utils#1126](https://github.com/nodejs/node-core-utils/pull/1126) - Fixed security release preparation behavior.

These changes reduce manual scanning of private release PRs and make the CLI
derive release preparation work from the same metadata used by the web viewer.
This is important because the release process now has to track reports,
dependencies, affected release lines, CVE trailers, backport PRs, and
announcement metadata consistently across tools.

### Node.js Security Process Documentation

Node.js documentation was updated so maintainers know how to label HackerOne
reports that represent dependency updates:

* [https://github.com/nodejs/node/pull/64634](https://github.com/nodejs/node/pull/64634)

A follow-up documentation PR was opened to update the security release
preparation instructions for the new `git node release --prepare --security`
behavior:

* [https://github.com/nodejs/node/pull/64699](https://github.com/nodejs/node/pull/64699)

The updated command flow allows `--security` to point directly at
`vulnerabilities.json` or at the security-release repository root. Reports and
dependency updates are then selected automatically from the `affectedVersions`
mapping for the release line being prepared.

## Security Release Operations

The July release was also used as an end-to-end validation of the new process:

* Created the active release tracking PR in the private security-release
  repository.
* Used the viewer and CLI together to review selected HackerOne reports,
  assign severity and CVSS metadata, prepare team summaries, and sync release
  metadata.
* Requested CVEs through the improved automation.
* Prepared pre-release and post-release website changes.
* Coordinated release volunteers across affected release lines.
* Tracked private fix and backport PR readiness per release line.
* Added dependency update support to the release metadata and preparation flow.
* Validated CI and Jenkins readiness before release publication.

This work turns the security release process from a collection of manual CLI
steps into a local, metadata-driven operations workflow while preserving the
existing Node.js security release model and keeping private report state out of
public release archives.

## Community and Governance

Continued active participation in the core Node.js and OpenJS security
coordination forums:

* Participated in Node.js Technical Steering Committee calls, including
  discussions relevant to release process, security operations, and project
  governance.
* Participated in Node.js Security Working Group discussions, supporting
  vulnerability triage, security release readiness, and ongoing process
  improvements.
* Participated in OpenJS Security Collab Space meetings, coordinating with the
  broader OpenJS security community on shared security practices, project
  support, and ecosystem-level security collaboration.

## July PR Review

GitHub activity for July was reviewed across RafaelGSS-authored PRs. The
OpenJS-relevant work included:

* 10 merged `node-core-utils` PRs supporting security release automation.
* 2 merged private `security-release` web viewer PRs, plus the active release
  tracking PR.
* 2 public `nodejs.org` PRs for security release communication.
* 2 public `nodejs/node` documentation PRs related to HackerOne dependency
  metadata and the updated security release preparation command.
* Multiple private Node.js release-line PRs for the July security release.

Unrelated personal project PRs were excluded from this report.
