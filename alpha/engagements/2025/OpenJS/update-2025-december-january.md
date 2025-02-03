# Update December 2024-January 2025

This report summarizes the accomplishments made during December 2024 and January 2025 within the Node.js project, spanning security initiatives, automation, community engagements, and release processes.

## Node.js

### Node.js Maintainers Threat Model

The Node.js team has published its first [Maintainers Threat Model](https://github.com/nodejs/security-wg/blob/main/MAINTAINERS_THREAT_MODEL.md), providing a clear overview of access control within the project. This model is structured as a table that outlines which roles have access to specific resources, including permissions that could allow injecting malicious code into the Node.js binary.

This initiative enhances transparency and helps both contributors and the wider ecosystem understand the security posture of Node.js maintainership. By explicitly defining access levels, the community can better assess risks and implement safeguards where necessary.

Example:

| Resource | External people | Contributors - Core/Triagers/WG | Build - Test/Infra/Admin | Admin - TSC/Releasers/Moderation | Security Stewards/Triagers/External | GitHub - Actions/Plugins |
|-         |-                |-                                |-                         |-                                 |-                                    |-                         |
| **HackerOne**                | - | -\-\- | -\-\- | aw-  | www   | -\- | 
| **MITRE**                    | - | -\-\- | -\-\- | a-\- | w-\-  | -\- | 
| **private/node-private**     | - | -\-\- | www   | aw-  | w-w   | -\- |
| **private/security-release** | - | -\-\- | -\-\- | a-\- | ww-   | -\- |
| **private/secrets**          | - | -\-\- | www   | a-\- | -\-\- | -\- |
| **nodejs/node**              | r | wrr   | rrw   | awa  | rrr   | wr  |

### Automating Node.js Releases and Security Releases

The Node.js release process has been significantly improved through automation, streamlining both regular and security releases. Recent enhancements ensure greater consistency, reduce manual effort, and minimize the risk of human error.

#### **Major Update: Automated Release Proposal Creation**

A key improvement is the introduction of a **GitHub Action that automates release proposal creation**, triggered via `workflow_dispatch`. This allows maintainers to generate a release proposal for a selected branch with minimal manual intervention. This functionality was implemented in [#55690](https://github.com/nodejs/node/pull/55690) and required updates in:
- [#862](https://github.com/nodejs/node-core-utils/pull/862)
- [#863](https://github.com/nodejs/node-core-utils/pull/863)
- [#864](https://github.com/nodejs/node-core-utils/pull/864) 

This automation has been incorporated into the [**official release documentation**](https://github.com/nodejs/node/blob/main/doc/contributing/releases.md), making it easier for contributors to follow a standardized and efficient process.

#### **Other Key Improvements**

- **Automated website banner updates** after a release ([#878](https://github.com/nodejs/node-core-utils/pull/878), [#886](https://github.com/nodejs/node-core-utils/pull/886))
- **Improved security release workflows**, including better handling of impacted versions and branch selection ([#885](https://github.com/nodejs/node-core-utils/pull/885), [#889](https://github.com/nodejs/node-core-utils/pull/889))
- **Fixes for `git node security --request-cve`** and CVE handling in changelogs ([#888](https://github.com/nodejs/node-core-utils/pull/888), [#174](https://github.com/nodejs/changelog-maker/pull/174))
- **Resolved issues in blog post generation** for security and dependency updates ([#887](https://github.com/nodejs/node-core-utils/pull/887), [#896](https://github.com/nodejs/node-core-utils/pull/896))
- **Better handling of PR statuses** in automation scripts ([#892](https://github.com/nodejs/node-core-utils/pull/892))
- **Various fixes in release tooling**, including base branch corrections and workflow optimizations ([#56617](https://github.com/nodejs/node/pull/56617), [#56200](https://github.com/nodejs/node/pull/56200))

These changes make the release process more efficient while ensuring that security patches and updates are managed with greater reliability.

### Node.js Permission Model is Now Stable

The Node.js Permission Model, introduced in v20.0.0, has matured and is now considered stable. This upgrade from **1.1 (Active Development)** to **2.0 (Stable)** marks a significant step forward in security controls within Node.js.

Over the past releases, several improvements and fixes have been made to refine the model, including:

- **Handled `fs.readdir({ recursive: true })` sync** ([#56041](https://github.com/nodejs/node/pull/56041))
- **Fixed duplicate path handling in the Permission Model** ([#56591](https://github.com/nodejs/node/pull/56591))
- **Clarified fork inheritance behavior for Permission Model flags** ([#56523](https://github.com/nodejs/node/pull/56523))
- **Backported fixes:** [#55797](https://github.com/nodejs/node/pull/55797), [#55697](https://github.com/nodejs/node/pull/55697)

With these updates, the model aligns with a **Defense in Depth** approach—enhancing security while recognizing that no single feature can fully prevent unauthorized code execution. One known limitation remains—symlink handling—but this is a broader challenge for any permission system based on file paths.

Despite this, the Permission Model is highly effective in reducing risk and providing guardrails for development and controlled environments.

For more details, see the [official documentation](https://nodejs.org/api/permissions.html).

### The  Package is-my-node-vulnerable Donated to the Node.js org

In December 2024 the package has been `is-my-node-vulnerable` has been donated to the Node.js org. https://github.com/nodejs/admin/issues/937

### Node.js Security Release

On January 21, 2025, Node.js released a security patch affecting four active release lines of Node.js.

- **CVE-2025-23083** (High)
- **CVE-2025-23084** (Medium)
- **CVE-2025-23085** (Medium)

However, with this release, the Node.js team also issued CVEs for End-of-Life (EOL) versions of Node.js

The project previously discussed and announced on the [Node.js blog](https://nodejs.org/en/blog/vulnerability/upcoming-cve-for-eol-versions) the approach of publishing CVEs for EOL versions. The intent is to raise awareness among users that EOL versions of Node.js almost cerntainly are subject to security vulnerabilities. The project does not accept vulnerability reports for EOL versions and it does not review EOL versions when reviewing vulnerabilities reported against supported versions.

- **CVE-2025-23087** targets Node.js v17 and all prior versions (starting with v0.x).
- **CVE-2025-23088** targets Node.js v19.
- **CVE-2025-23089** targets Node.js v21.

### **Security, Automation, and Tooling Updates** 

Several improvements have been made across the Node.js project, focusing on security, automation, and developer tools: 

#### **Security and Documentation** 
- Created the `@nodejs/security-stewards` team to improve coordination on security-related tasks ([#943](https://github.com/nodejs/admin/issues/943)). 
- Added code owners for the security release process to ensure clear responsibility ([#56521](https://github.com/nodejs/node/pull/56521)).

#### **Security Tools and CVE Management** 
- Fixed issues in `nodejs-cve-checker` to improve how vulnerabilities are tracked ([#9](https://github.com/nodejs/nodejs-cve-checker/pull/9)).
- Introduced `npx-safe`, an alias for `npx` that enables the Permission Model by default to limit package execution risks ([Announcement](https://x.com/_rafaelgss/status/1881394699837272496)).

#### **Release and Development Improvements**
- Added `--disable-sigusr1` to prevent the signal I/O thread from starting when not needed ([#56441](https://github.com/nodejs/node/pull/56441)).
- Created a GitHub Action to remind maintainers about upcoming major releases ([#56199](https://github.com/nodejs/node/pull/56199)).

These updates make security processes clearer, improve automation, and add useful tools for developers.

## Ecosystem

### Security Compliance Guide (tooling)

In 2024, the team developed a [POC for a "Dashboard"](https://www.youtube.com/embed/B1kd8k5SvBI) to showcase how compliance insights could streamline maintainers' workflows based on feedback collected from the pilot program. At this stage, the key integrations included GitHub APIs and a few compliance checks from [the OpenJS Security Compliance Guide v1](https://openpathfinder.com/docs/history/#4-the-dashboard-poc-november-2024).

Following the success of the Dashboard POC, the team decided to formalize and expand its efforts, leading to the creation of [OpenPathfinder](https://openpathfinder.com/). This new organization empowers maintainers to use these tools and contribute to their development.

The [history of OpenPathfinder](https://openpathfinder.com/docs/history) traces its evolution from a security compliance guide to a comprehensive initiative.

#### Tools under active development so far:
- **[VisionBoard](https://openpathfinder.com/docs/visionBoard):** A CLI tool that connects to external resources, such as GitHub APIs and [the OSSF Scorecard](https://openpathfinder.com/docs/visionBoard/providers#ossf-scorecard), to query, store, and analyze project data for compliance. This tool builds upon the Dashboard POC.
- **[FortSphere](https://openpathfinder.com/docs/fortSphere):** A CLI tool focused on enhancing GitHub repository and organization management through streamlined security policies.

A [new website](https://openpathfinder.com/docs/getting-started) provides access to:
- **[Policies](https://openpathfinder.com/docs/fortSphere/policies)**
- **[Checklists](https://openpathfinder.com/docs/visionBoard/checklists)**
- **[Checks](https://openpathfinder.com/docs/visionBoard/Checks)**
- Detailed information on [the project architecture](https://openpathfinder.com/docs/visionBoard/architecture), usage and much more.

In this [blog post](https://openpathfinder.com/blog/welcome/), you’ll find a 10-minute demo showcasing the current capabilities of VisionBoard and FortSphere. 

For VisionBoard’s future roadmap, check [this issue](https://github.com/OpenPathfinder/visionBoard/issues/30).

### Security Compliance Guide v1.1 Improvements

* Began early work to iterate to [v1.1 of the Compliance Guide](https://docs.google.com/spreadsheets/d/1GwIsAudAn89xv9DAbr1HUaY4KEVBsYfg--_1cW0uIB0/edit?pli=1&gid=1617559049#gid=1617559049) based on feedback from maintainers. Expect an in-depth update in February.

### OpenJS CVE Numbering Authority (CNA) Launch

- Scheduled 6 virtual townhalls for OpenJS maintainers to review the CNA's launch and operations plans, answer questions, and hear requests and feedback.
- Distributed the [OpenJS CNA Guide for OpenJS Maintainers](https://docs.google.com/document/d/1AID4IacA-58UzJYe2FC76knEuABWZ37L-a4KiYJ_bm4/edit?usp=sharing) (which will transition to GitHub after updates from the townhalls.
- Updated the [OpenJS CVD Guide](https://github.com/openjs-foundation/security-collab-space/tree/main/CVD_Guide) based on feedback from the OpenJS Security Collab Space. Expect more updates in February.
- Initial design for a new [OpenJS Security page](https://github.com/openjs-foundation/security-collab-space/issues/266) in addition to the CNA page to highlight resources for project consumers and maintainers.
