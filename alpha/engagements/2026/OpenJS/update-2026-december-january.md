# Update December 2025-January 2026

This report summarizes the accomplishments made during December 2025 and January 2026 within the OpenJS Ecosystem and Node.js project, spanning security initiatives, automation, community engagement, and release engineering.

## Node.js

### Security Vulnerability Triage and Patching

Multiple HackerOne vulnerability reports were reviewed and addressed during this period:

* **Permission Model - Symlink disable**: Addressed a reported issue related to symlink handling in the Permission Model on Windows, ensuring consistent behavior across platforms.
* **Unsafe Buffer**: Triaged and patched a report concerning unsafe Buffer usage patterns.
* **TLSSocket Patch**: Resolved a vulnerability report related to TLSSocket behavior.
* **Permission Model futimes**: Fixed a security issue involving `futimes` operations within the Permission Model, ensuring file timestamp modifications are properly gated by permission checks.
* **Ongoing report reviews**: Continued triaging incoming HackerOne reports and coordinating disclosure processes.

### Node.js Security Release

Prepared and coordinated the [January 13, 2026 Node.js security release](https://nodejs.org/en/blog/vulnerability/december-2025-security-releases), including synchronizing security branches across active release lines. This release addressed 3 high severity, 4 medium severity, and 1 low severity issues across the 25.x, 24.x, 22.x, and 20.x release lines. A separate [advisory for DoS mitigation related to async hooks stack exhaustion](https://nodejs.org/en/blog/vulnerability/january-2026-dos-mitigation-async-hooks) was also published for React, Next.js, and APM users. Additionally, an [OpenSSL Security Advisory assessment](https://nodejs.org/en/blog/vulnerability/openssl-fixes-in-regular-releases-jan2026) was published covering the impact of 12 OpenSSL CVEs on Node.js.

### Permission Model Improvements

* **Increased test coverage** for the Permission Model: [nodejs/node#60746](https://github.com/nodejs/node/pull/60746)
  * Strengthened the test suite to cover additional edge cases and ensure reliability of the permission enforcement layer.

### Threat Model and Documentation

* **Clarified threat model API exposures**: Updated the Node.js threat model documentation to better define the security boundaries around API surface exposures, helping maintainers and users understand which scenarios are in-scope for security reports.
* **Added CVE delay mention**: Updated security release documentation to include information about potential CVE publication delays, improving transparency around the disclosure timeline.

### OpenSSL Advisory Review

Reviewed the latest OpenSSL security advisory to assess its potential impact on Node.js and dependent projects, ensuring timely awareness and response planning.

### VEX File for Node.js

Continued work on implementing VEX (Vulnerability Exploitability eXchange) files for Node.js, coordinated with Marco. VEX files help downstream consumers accurately assess which reported CVEs are actually exploitable in their Node.js deployments, reducing false-positive noise.

### Security Automation and Tooling

Several improvements were made to the Node.js security release automation and tooling:

* **Automated CVE ID handling**: Enhanced the security release tooling to handle `cveId` fields automatically, reducing manual steps during security release preparation.
* **Adjusted `--request-cve`**: Refined the `--request-cve` command in node-core-utils to improve CVE request workflows.
* **Added `--newVersion` mention**: Updated tooling documentation to include the `--newVersion` flag for security release workflows.
* **Request PR-URL metadata on security backports**: Enforced PR-URL metadata on security backport commits for better traceability and audit trails.
* **Fixed Node.js vulnerability sync DB generation**: Resolved issues in the nodejs-dependency-vuln-assessments repository to restore accurate vulnerability database generation.
* **Listed security-team in Node.js core**: Integrated the `security-team` listing into Node.js core governance, improving coordination on security-related tasks.

### Release Engineering

* **Node.js v25 release**: Shipped a new release in the v25.x line, continuing the focus on secure-by-default applications and runtime modernization.

## OpenJS Ecosystem

### Fastify Threat Model Enhancement

Enhanced the Fastify threat model documentation, extending the adoption of structured threat models across the OpenJS ecosystem. Following the earlier success with Express, Lodash, and Webpack, Fastify now has improved guidance on security boundaries and expected behaviors.

### Secure npm Publishing Guide v2

Updated the secure npm publishing guide to v2, building on the initial guidance published in November 2025. The updated guide provides refined recommendations for maintainers on secure publishing workflows, including trusted publishing and CI-based approaches.

### MDN Documentation Update

Updated the MDN Web Docs page related to Node.js security features, ensuring that the broader web developer community has access to accurate and current information about Node.js security capabilities.

### HackerOne Signal Requirement

Published a [blog post announcing the new HackerOne Signal requirement](https://nodejs.org/en/blog/announcements/hackerone-signal-requirement) for Node.js vulnerability reports, requiring a minimum Signal of 1.0 to submit reports. This change was driven by an increasing trend of invalid submissions — over 30 reports were received during the December 15 to January 15 holiday period alone, creating a triaging burden beyond what the team could process. Researchers below the threshold can still reach the security team through the OpenJS Foundation Slack. This initiative is part of an ongoing discussion about improving the quality of vulnerability reports and reducing noise for security maintainers, which has been actively discussed in the Node.js Vulnerability Working Group meetings during this period.

### Vulnerability Working Group Participation

Participated in Node.js Vulnerability Working Group meetings to discuss the HackerOne Signal requirement changes and broader strategies for improving vulnerability report quality. These discussions focused on balancing accessibility for security researchers with the need to reduce the triaging burden on maintainers, and evaluating the impact of the new Signal threshold on the project's security posture.

### Webpack Security Triage Team

Supported the establishment of a dedicated security triage team for Webpack (https://github.com/webpack/security-wg/pull/17), furthering the goal of structured security governance across OpenJS Foundation projects.

### Lodash Security Reset

Coordinated the Lodash security reset (https://socket.dev/blog/inside-lodash-security-reset, https://openjsf.org/blog/lodash-security-overhaul), applying best practices from the OpenJS Foundation projects. This effort included releasing CVE-2025-134655 under the OpenJS Foundation CNA, marking a significant step in bringing Lodash's security posture in line with foundation standards.

### Community Engagement

* **Recorded educational shorts** for the OpenJS Foundation YouTube channel, promoting security awareness and best practices across the JavaScript community.
* **Completed End of Year Alpha Omega reporting**, summarizing the 2025 engagement accomplishments and outcomes.
