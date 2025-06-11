# Update April 2025

This report summarizes the accomplishments made during April 2025 within the Node.js project, spanning security updates, CI improvements, release preparations, and educational initiatives.

## Node.js

### Security Releases for Node.js 18, 20, and 22

In April, the Node.js project published security releases for versions 18, 20, and 22. These updates addressed vulnerabilities across core dependencies, including:

* **Undici**: An updated version with security fixes was incorporated.
* **c-ares**: Security-related patches were integrated into all supported release lines.

These updates were coordinated following the standard security release process and communicated through official Node.js channels.

### CodeQL Integration

Static code analysis via [GitHub CodeQL](https://codeql.github.com/) has been enabled for the Node.js codebase:

* [https://github.com/nodejs/node/pull/57788](https://github.com/nodejs/node/pull/57788)

This integration enhances our ability to detect potential security issues early in the development lifecycle by leveraging GitHub’s semantic analysis tooling.

### Node.js Permission Model – Developer Experience Enhancements

Improvements to the experimental [Permission Model](https://nodejs.org/api/permissions.html) were introduced to improve developer experience. When a `ERR_ACCESS_DENIED` error is thrown, Node.js now suggests appropriate `--allow-` flags:

* [https://github.com/nodejs/node/pull/57585](https://github.com/nodejs/node/pull/57585)

This update aims to reduce friction when adopting fine-grained permissions in applications.

### Security Incident Disclosure – CI Infrastructure

A full disclosure blog post was published detailing the March 2025 [CI security incident](https://nodejs.org/en/blog/vulnerability/march-2025-ci-incident), which affected test infrastructure used in the Node.js project. The post outlines:

* Timeline of the incident
* Remediation actions taken
* Long-term prevention measures

This transparency is part of our commitment to improving security practices within the Node.js ecosystem.

### Hardening GitHub Actions – Best Practices Blog Post

A concise guide was published summarizing lessons learned from the GitHub Secure Open Source course and how they apply to GitHub Actions:

* [https://blog.rafaelgss.dev/securing-github-actions](https://blog.rafaelgss.dev/securing-github-actions)

The blog highlights actionable steps to mitigate common attack vectors in CI/CD pipelines and has been shared with contributors and integrators across the ecosystem.

### Node.js 24 Release Coordination

Final preparations for the release of **Node.js v24.0.0** have been underway. Release coordination includes:

* Changelog curation
* Release candidate validation
* Final review of breaking changes and documentation

The official release is targeted for **May 6, 2025**:

* [https://github.com/nodejs/node/pull/57609](https://github.com/nodejs/node/pull/57609)

## OpenJS Security Collab Space

### Security Compliance Guide

#### Upcoming Changes

As expected, the Security Compliance Guide is being frequently updated as it is undergoes initial use. In the Guide's first [v1.1 update in March](https://docs.google.com/spreadsheets/d/1GwIsAudAn89xv9DAbr1HUaY4KEVBsYfg--_1cW0uIB0/edit?gid=924266915#gid=924266915), we focused primarily on adding new and more purposeful guidance for using npm. Work continues on a larger 2.0 update that will:

- Incorporate feedback from the Node.js team, who were the first big adopters of the Guide.
- Align the Guide's data structure with VisionBoard's.
- Assess each guideline for automated testability and determine a guideline strategy that balances security best practices and automated control testing and monitoring.

#### Impact on Outreach

With the completion of v1.1 of the Compliance Guide, broader outreach to Projects for compliance surveying is planned to begin in early May.

### VisionBoard@1.0.0 active development

The [VisionBoard project (OpenPathFinder) advanced toward](https://openpathfinder.com/blog/visionboard-update-may-2025) its [v1.0.0 milestone](https://github.com/orgs/OpenPathfinder/projects/3/views/3?query=sort%3Aupdated-desc+is%3Aopen) this month, introducing updates aligned with secure development and deployment practices. Highlights include:

* A new Express-based web server with scoped API routing and graceful startup/shutdown handling.
* Dynamic website rendering with EJS templates, supporting both static and dynamic report generation.
* Hardened Docker workflows with health checks and non-root containers.
* CI improvements using Playwright for end-to-end tests with GitHub Actions integration.

These updates improve reliability, security, and maintainability across the platform.

### Node.js and the OpenJS Security Compliance Guide

The Node.js Security Working Group made significant progress this month toward adopting the Security Compliance Guide v1.0. In addition, the team has provided key feedback that is actively informing the design of version 2.0, which is currently under development.

Beyond compliance efforts, the group is contributing to the direction and feature planning of two ecosystem tools: [VisionBoard@1.0.0](https://openpathfinder.com/docs/visionBoard) and [fortSphere@1.0.0](https://openpathfinder.com/docs/fortSphere). These collaborations aim to improve how projects track security posture, automate reporting, and align with evolving best practices.

The goal is to gather feedback through real-world usage and make these tools more useful and adaptable for other maintainers and projects—similar to the community-driven approach taken during the development of the [OSSF Scorecard Monitor](https://github.com/ossf/scorecard-monitor) and [OSSF Scorecard Visualizer](https://github.com/ossf/scorecard-visualizer).

Discussion and ongoing work can be followed in [issue #1440](https://github.com/nodejs/security-wg/issues/1440).

### OpenJS CVE Numbering Authority (CNA) Launch Delays

We are awaiting further guidance from Red Hat on next steps to launch the CNA.

### Secure Releases Guide v2

The Collab Space has aligned on the scope for the first (v2) update to the [OpenJS Secure Releases Guide](https://github.com/openjs-foundation/security-collab-space/blob/main/secure-releases.md). The first content update will focus on securely publishing to npm. This content is intended to also be used to update the [OpenSSF's npm Best Practices Guide](https://github.com/ossf/package-manager-best-practices/blob/main/published/npm.md).
