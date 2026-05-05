# OpenJS Foundation Security Update: April 2026

*Covering April 2026 | Powered by the Alpha-Omega Partnership*

April was a month of strategic planning and community engagement, centered around the Node.js Collaborators Summit in London. The focus shifted toward long-term sustainability improvements, including addressing AI-driven report challenges, refining the Permission Model, and preparing for the Node.js 26.0.0 release.

## Node.js Collaborators Summit - London

Participated in the Node.js Collaborators Summit in London, hosting three key sessions and engaging in Technical Steering Committee discussions:

* **Node.js Security and Next Steps (90 minutes)**: Led comprehensive discussion on security priorities, ongoing challenges with AI-generated reports, and strategic direction for Node.js security
* **New Release Schedule (30 minutes)**: Facilitated session on the upcoming release strategy changes effective with Node.js 27
* **libuv v2 Impact (30 minutes)**: Discussed the implications of libuv v2 for Node.js and the ecosystem
* Active participation in all other summit discussions as a TSC member

## Quarterly Reporting

Published the Q1 2026 quarterly report covering December 2025 through March 2026. The report provides comprehensive coverage of:
* 17 Node.js CVEs addressed across two major security releases
* 18 ecosystem CVEs published through OpenJS CNA operations
* Permission Model advances including the new `--permission-audit` flag
* Bug bounty program pause and sustainability challenges
* New Node.js release strategy for long-term maintainability

## Addressing AI-Generated Report Challenges

The surge in AI-generated security reports continues to impact triage workflows. Several initiatives are underway to address this:

* **AI.md Guidelines**: Discussing addition of an AI.md file to Node.js repository to reduce AI "slop" in reports and set clear expectations for AI-assisted contributions
* **Contributing Guidelines Update**: Working on adding AI-specific guidelines to Node.js contributing documentation
* **LLM Report Classifier**: Developing an automated classifier for security reports (nodejs/security-wg#1554) to help identify and triage AI-generated submissions more efficiently
* **HackerOne Bot Fix**: Fixed a bug in the HackerOne bot that handles incoming security reports, improving automated triage workflows

## Permission Model Development

Continued advancement of the Permission Model with bug fixes and new capabilities:

* **Permission Audit Bug Fix (PR #63047)**: Fixed issues in the `--permission-audit` mode to ensure reliable observability
* **permission.drop Feature (PR #62672)**: Added new `permission.drop` API allowing applications to programmatically reduce their own permissions at runtime, enabling principle of least privilege patterns

## Security Process Evolution

### Embargo Policy Discussion

Ongoing discussion in TSC about ending the embargo policy for security reports. This controversial proposal addresses:
* Most AI-discovered issues are effectively public already (anyone with an LLM can find them)
* Private queues slow down fixes that could benefit from community visibility
* Volunteer sustainability challenges with current private workflow
* Need for defined embargo process for truly sensitive issues

The discussion continues via TSC emails with community input.

## Node.js Core Development

### ABI Stability Discussion

Key technical discussion about whether to drop ABI (Application Binary Interface) stability guarantees in major versions. This would allow more flexibility for improvements but impact native addon compatibility.

### UV_THREADPOOL_SIZE Increase

Raised the default UV_THREADPOOL_SIZE for Node.js 27, improving performance for I/O-heavy workloads out of the box.

### Node.js 26.0.0 Release Preparation

Significant time invested in preparing the Node.js 26.0.0 release, including:
* Coordinating release timeline
* Testing and validation
* Documentation updates
* Release tooling improvements

## GitHub Secure Open Source Fund

Participated in GitHub's Secure Open Source check-in meetings, discussing:

* Progress on security initiatives
* Funding utilization and impact
* Future priorities and resource needs
* Collaboration opportunities with other funded projects