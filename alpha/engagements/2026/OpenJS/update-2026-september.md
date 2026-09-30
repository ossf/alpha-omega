# OpenJS Foundation Security Update: September 2026

*Covering September 2026 | Powered by the Alpha-Omega Partnership*

This month's work focused on Node.js permission model documentation and review, security release preparation, dependency vulnerability assessment cleanup, release infrastructure maintenance, community sessions, and security skills exploration. Below is a summary of completed items across Node.js core, release tooling, dependency assessment, infrastructure, and community engagement.

## Node.js Permission Model & Core Reviews

Permission model scope, labeling, and related Node.js core reviews were completed.

- **doc: clarify permission model scope for output paths**: Clarified the permission model scope for output paths.
  - [PR #66004](https://github.com/nodejs/node/pull/66004) (Completed Sep 14)
- **meta: label permission model changes correctly**: Labeled permission model changes correctly.
  - [PR #66208](https://github.com/nodejs/node/pull/66208) (Completed Sep 24)
- **Review of nodejs/node#65359**: Reviewed nodejs/node#65359.
  - [PR #65359](https://github.com/nodejs/node/pull/65359) (Completed Sep 23)
- **Review of nodejs/node#66132: src,lib: add --allow-env permission**: Reviewed the PR adding the `--allow-env` permission to the Node.js permission model.
  - [PR #66132](https://github.com/nodejs/node/pull/66132) (Completed Sep 25)
- **Review of nodejs/node#65411: fs: fix repeated copy of directory with symlinks**: Reviewed the fix for repeated copy of a directory with symlinks.
  - [PR #65411](https://github.com/nodejs/node/pull/65411) (Completed Sep 25)

## Security Release Pipeline & Release Infrastructure

Security release tooling and release infrastructure maintenance continued.

- **Security release preparation**: Added security release preparation in `node-core-utils`.
  - [nodejs/node-core-utils#1197](https://github.com/nodejs/node-core-utils/pull/1197) (Completed Sep 23)
- **Upcoming Node.js security release preparation**: The upcoming Node.js security release was prepared. (Completed Sep 25)
- **keyring: update expiry for RafaelGSS key**: Updated the expiry for the RafaelGSS key in the release keyring.
  - [nodejs/release-keys#59](https://github.com/nodejs/release-keys/pull/59) (Completed Sep 9)
- **fix: accept CVE IDs with 4 or more sequence digits**: Fixed CVE ID handling for IDs with 4 or more sequence digits.
  - [nodejs/commit-stream#26](https://github.com/nodejs/commit-stream/pull/26) (Completed Sep 22)

## Dependency Vulnerability Assessment

Dependency vulnerability assessment work focused on reducing false positives and aligning checks with supported versions.

- **Update dependencies for security**: Updated `nodejs/nodejs-dependency-vuln-assessments` to reduce false positives and keep checks aligned to supported versions.
  - [nodejs/nodejs-dependency-vuln-assessments issues](https://github.com/nodejs/nodejs-dependency-vuln-assessments/issues) (Completed Sep 24)
- **fix: stop querying NVD for nbytes by keyword**: Stopped querying NVD for nbytes by keyword.
  - [nodejs/nodejs-dependency-vuln-assessments#427](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/427) (Completed Sep 23)
- **fix: ignore CVEs that don't affect Node.js**: Ignored CVEs that do not affect Node.js.
  - [nodejs/nodejs-dependency-vuln-assessments#435](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/435) (Completed Sep 23)
- **fix: filter reviewed ngtcp2 CVEs by bundled version**: Filtered reviewed ngtcp2 CVEs by bundled version.
  - [nodejs/nodejs-dependency-vuln-assessments#437](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/437) (Completed Sep 23)
- **fix: ignore HdrHistogram Java vulnerabilities**: Ignored HdrHistogram Java vulnerabilities.
  - [nodejs/nodejs-dependency-vuln-assessments#438](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/438) (Completed Sep 23)
- **fix: ignore zlib CRC combine vulnerability**: Ignored the zlib CRC combine vulnerability.
  - [nodejs/nodejs-dependency-vuln-assessments#439](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/439) (Completed Sep 23)

## Security Skills Exploration

Exploratory work looked at whether a Node.js security skills module would make sense.

- **Node.js security skills feasibility check**: Evaluated whether it makes sense to create a skills module focused on Node.js security.
  - [Node.js security skills draft](https://github.com/RafaelGSS/nodejs-security-skills/blob/main/SKILL.md) (Completed Sep 25)

## Community Engagement

Community work centered on talks and Collaborator Summit preparation.

- **ParaibaJS talk**: Presented at ParaibaJS. (Completed Sep 8)
- **Create Collab Summit session**: Created a Collab Summit session.
  - [openjs-foundation/summit#514](https://github.com/openjs-foundation/summit/issues/514) (Completed Sep 17)
- **Node.js Collaborator Summit Proposal**: Prepared a deck for review for the Node.js Collaborator Summit proposal.
  - [Draft proposal PR](https://github.com/RafaelGSS/node-security-operating-model/pull/1) (Completed Sep 26)
- **NodeConfEU Slides**: Prepared the NodeConfEU slides.
  - [NodeConfEU slides](https://docs.google.com/presentation/d/1yIcCVqeBjCJltsTuJ9WRu8AK4KOBQnGc4poKxkUfbsw/edit?usp=sharing) (Completed Sep 27)
