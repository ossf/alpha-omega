# Update June 2026

This report summarizes the accomplishments made during June 2026 within the OpenJS Ecosystem and Node.js project, spanning security releases, release process automation, Permission Model improvements, AI-assisted report triage, and CNA tooling.

## Node.js

### June Security Release

The Node.js project prepared and coordinated a major June security release addressing **18 vulnerabilities** across all active release lines.

This release was significantly larger than a typical Node.js security release:

* **13 total patches** were included, compared with the previous norm of roughly 6-7 patches per security release.
* Rafael continued maintaining and improving the security release automation.
* Antoine joined Rafael to run through the full release process using the tooling, validating that the process can be executed by more than one maintainer.

This was an important operational milestone because it demonstrated that the security release process is becoming easier to document, share, and eventually hand off across the security team.

### Security Release Automation

Several improvements were made to the Node.js security release workflow.

* **Security release web viewer**: Added a visual interface for the security release process, showing which reports are included, what information is missing, and the checklist status for each release line. This is especially important as security releases grow beyond what is practical to manage entirely from the terminal.
* **LLM-assisted report validation**: Integrated report validation into the release viewer. When a report is queued for inclusion, the tooling analyzes it against the Node.js threat model, prior accepted CVEs, CWE patterns, and historical report context, returning a confidence assessment and CVSS estimate for maintainer review.

The tooling remains in beta. The next security release will be used as a real-world test of the updated process, with documentation and a walkthrough video planned for the security team.

### Security Embargo Policy Change

Node.js no longer requires a security embargo for most security patches.

Previously, the Node.js Jenkins CI environment had to be locked down to TSC-only access during security release preparation. This meant a fix could not be tested in CI until the embargo window was opened, and patches written weeks or months earlier could fail during the release crunch.

The new workflow restricts Jenkins read-only access to collaborators only. Because only collaborators can see logs and build artifacts, running CI on a security fix no longer creates the same information leak risk. Contributors can now write and test a patch when a report arrives instead of waiting for an embargo window.

Work reference: https://github.com/nodejs/security-wg/pull/1570

### Permission Model Improvements

The Permission Model continued to gain practical production features during Q2, with June work focused on adoption and runtime security impact.

* **`--permission-audit` mode**: Allows teams to evaluate the Permission Model without enforcing restrictions. Instead of throwing access errors, Node.js emits permission check events through the diagnostics channel so applications can observe required permissions before enabling enforcement.
* **`permission.drop()`**: Allows an application to reduce its own permissions at runtime after initialization, supporting least-privilege patterns for production workloads.

Ulises published an analysis explaining why install-time protections alone are insufficient and why runtime permission constraints remain important for npm ecosystem security.

Work reference: https://nodesource.com/blog/npm-v12-install-scripts-not-a-silver-bullet

### AI-Assisted Security Report Triage

The Node.js security team continued addressing the increase in AI-assisted vulnerability reports.

Recent report volume shows the scale of the problem:

* 352 HackerOne reports were received over the two years before this quarter.
* February 2026 report volume increased 4.6x.
* March 2026 had 65 reports in a single month.

Several mitigations moved forward:

* **HackerOne report template update**: Reproducible examples must now be provided in JavaScript, reducing maintainer time spent translating reports from Python or other languages before triage.
* **LLM report classifier**: A dedicated classifier is in development with IBM support to assess incoming HackerOne reports before human review.
* **Node.js security release report validation**: Rafael's parallel LLM-assisted validation prototype is already being used by the Node.js security team and was integrated into the June security release web viewer.

### AI Contribution Policy

The Node.js project formalized guidance for AI-assisted contributions during the spring, with continued relevance for security review in June.

Key outcomes:

* Pull requests are expected to stay under 5,000 lines, regardless of whether AI was used.
* DCO sign-off is being enforced more strictly.
* Large AI-generated pull requests are being discouraged because they are not practically reviewable and can hide subtle behavioral changes.

### Node.js 26 and Release Schedule Follow-Up

June followed the May release of Node.js 26, the final major release under the long-running odd/even release model.

Starting with Node.js 27 in October 2026, every release line is expected to move toward LTS, version numbers will align with the calendar year, and the number of concurrent active release lines will shrink. This directly supports security sustainability by reducing the number of release lines requiring backports.

Node.js 26 also shipped with the Temporal API enabled by default, reducing reliance on third-party date libraries for applications that can adopt the native runtime API.

Work reference: https://gamma.app/docs/Nodejs-Security-jznd05udav90fp0

### ABI Stability Discussion

Discussion continued on whether Node.js should relax its longstanding V8 ABI stability commitment.

The current policy slows V8 upgrades because Node.js must preserve compatibility with how V8 structures are mapped in memory. Relaxing this policy would primarily affect projects that vendor Node.js into their own binaries, such as Electron, but would not affect most Node.js users.

The security benefit would be faster V8 adoption and reduced delay for V8 security patches. The discussion remains open and no final policy change has been adopted.

## OpenJS Ecosystem

### OpenJS CNA Operations

The OpenJS Foundation CNA passed its one-year milestone this quarter.

CNA activity has increased significantly:

* In the second half of 2025, the CNA published 3 CVEs.
* In the first half of 2026, the CNA published **49 CVEs**.
* Roughly 10 additional CVEs are in open review.

This growth reflects both increased advisory coordination work and the impact of AI-assisted scanning across the JavaScript ecosystem.

Work reference: https://cna.openjsf.org/security-advisories.html

### AI Security Engineer in Residence

Ulises Gascon joined Alpha-Omega as the OpenJS AI Security Engineer in Residence, with the role formally taking effect at the start of Q2.

His work spans:

* CNA operations
* Security triage tooling
* Ecosystem CVE coordination
* Advisory workflow automation
* CNA API design and prototyping

Work reference: https://alpha-omega.dev/blog/announcing-the-node-js-ai-security-engineer-in-residence/

### GHSA Dashboard

Ulises released the GHSA Dashboard, a self-hosted Grafana dashboard for GitHub Security Advisories.

The dashboard is designed for CNAs and maintainers coordinating disclosure across many repositories. It provides an 18-panel overview covering advisory state, severity, CVSS, CWE ranking, throughput over time, time-to-publish, and aging advisories in triage.

The implementation uses Postgres, mirrors the GitHub API into a single table, and runs with a small Node.js scraper and Grafana setup.

Work reference: https://github.com/UlisesGascon/ghsa-dashboard/releases/tag/v1.0.0

Demo: https://www.youtube.com/watch?v=HkePMUn0rKs&t=242s

### OpenJS CNA API Proof of Concept

Ulises demonstrated a proof-of-concept CNA API and client tooling at the OpenJS Security Working Group meeting on June 22.

The goal is to standardize how CVE records flow through OpenJS CNA operations by automating creation, routing, and publication of advisories instead of managing them through manual GitHub workflows.

The PoC is not the final implementation. It exists to align stakeholders on the operating model before production implementation begins.

Work references:

* https://github.com/UlisesGascon/openjs-cna-api-poc
* https://github.com/UlisesGascon/openjs-cna-api-poc/blob/main/docs/architecture.md
* https://github.com/UlisesGascon/openjs-cna-tools
* https://github.com/openjs-foundation/security-wg/issues/337

### Next Steps

The next Node.js security release will be used to further validate the updated release automation, web viewer, and LLM-assisted report validation workflow.

The CNA API PoC will move toward implementation planning. The LLM report classifier remains in beta. Documentation and operational handoff for the security release tooling will be a priority so more maintainers can participate in future releases.

The Node.js Collaboration Summit is planned for late September and will be an important entry point for contributors interested in Node.js security work.
