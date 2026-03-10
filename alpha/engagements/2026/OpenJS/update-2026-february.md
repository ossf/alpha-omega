# Update February 2026

This report summarizes the accomplishments made during February 2026 within the OpenJS Ecosystem and Node.js project, spanning security initiatives, automation, community engagement, and release engineering.

## Node.js

### Security Vulnerability Triage and Patching

Multiple vulnerability reports submitted through HackerOne were reviewed and handled during this period, with ongoing efforts to improve triage efficiency and the overall security reporting workflow.

* **HackerOne Report Validation**: Continued triaging and validating incoming HackerOne reports, ensuring that submitted issues are actionable, reproducible, and relevant to the Node.js codebase before progressing through the security workflow.

* **Review AWS Report**: Reviewed and assessed AWS-reported security issue #3407207 to determine potential impact on Node.js, including evaluating exploitability, affected components, and whether mitigation or fixes were required.

* **Improved Report Closure Validation**: Strengthened the validation process for closing security reports by ensuring that each closure includes appropriate verification, documentation, and confirmation that the issue does not represent a valid security vulnerability.

* **HackerOne Signal Requirement Update**: Updated the Node.js security process documentation and blog announcement to clarify the new HackerOne submission requirement. The project now requires reporters to have a **Signal score of 1.0 or higher** to submit vulnerability reports through HackerOne. This change was introduced to reduce the growing volume of low-quality or automated reports and allow the security team to focus on actionable vulnerabilities while maintaining sustainable triage operations. Researchers without sufficient Signal can still coordinate with the security team through alternative channels before filing a report.

Work reference: https://nodejs.org/en/blog/announcements/hackerone-signal-requirement

### Permission Model Observability Improvements

* **Permission Audit Mode and C++ Diagnostics Channel Integration (PR #61869)**: Advanced the Node.js Permission Model by introducing `--permission-audit`, a warning-only mode that allows applications to observe permission checks without blocking execution. Instead of throwing `ERR_ACCESS_DENIED`, Node.js emits permission check events through diagnostics channels so developers can inspect access decisions at runtime. The PR also adds C++ support for diagnostics channels, reducing unnecessary JS boundary crossings and making permission-related observability more efficient for native-side checks. This improves visibility into how the Permission Model behaves in real applications and helps developers evaluate adoption before enforcing restrictions.

### Documentation and Governance

* **Remove https://github.com/nodejs/TSC/blob/main/Security-Team.md**: Cleaned up outdated security team documentation from the TSC repository, consolidating security governance documentation.

### Community Engagement and Collaboration

* **Security Session for Collab Summit**: Organizing and facilitating a security-focused session at the Node.js Collaboration Summit to discuss current security initiatives and gather community feedback.
* **Release Session for Collab Summit**: Organizing a Node.js Release WG session to talk about the new Node.js release strategy.

### Node.js New Release Schedule

A new blog post scheduled for publication on April 2nd, 2026, announcing a significant change to how Node.js handles its release cycle, taking effect starting with Node.js 27.

Key changes being communicated:

* One major release per year (in April), with LTS promotion happening each October.
* Every release becomes LTS — the long-standing odd/even numbering distinction goes away (no more "odd = short-lived" releases).
* An "Alpha channel" replaces odd-numbered releases, intended for library authors and CI pipelines to test early. It uses nightly builds only (no formal alpha releases), and semver-major changes are permitted during this phase.
* The total support window per release is 36 months (6 months Alpha → Current → 30 months LTS).
* A full 10-year schedule table (v27–v36) is included.

We are actively discussing the security sustainability of the project and this change would help in that front.

### OpenJS CNA Operations

New CVEs were released:

- [CVE-2026-2359](https://www.cve.org/CVERecord?id=CVE-2026-2359) patched on `multer@2.1.0`. High-severity, vulnerable to DoS via resource exhaustion ([GHSA-v52c-386h-88mc](https://github.com/expressjs/multer/security/advisories/GHSA-v52c-386h-88mc))
- [CVE-2026-3304](https://www.cve.org/CVERecord?id=CVE-2026-3304) patched on `multer@2.1.0`. High-severity, vulnerable to DoS via incomplete cleanup ([GHSA-xf7r-hgr6-v32p](https://github.com/expressjs/multer/security/advisories/GHSA-xf7r-hgr6-v32p))
- [CVE-2026-2880](https://www.cve.org/CVERecord?id=CVE-2026-2880) patched on `@fastify/middie@9.2.0`. High-severity, vulnerable to path normalization inconsistency leading to auth bypass ([GHSA-8p85-9qpw-fwgw](https://github.com/fastify/middie/security/advisories/GHSA-8p85-9qpw-fwgw))
- [CVE-2026-3520](https://www.cve.org/CVERecord?id=CVE-2026-3520) patched on `multer@2.1.1`. High-severity, vulnerable to DoS via uncontrolled recursion ([GHSA-5528-5vmv-3xc2](https://github.com/expressjs/multer/security/advisories/GHSA-5528-5vmv-3xc2))
- [CVE-2026-3419](https://www.cve.org/CVERecord?id=CVE-2026-3419) patched on `fastify@5.8.1`. Moderate-severity, vulnerable to malformed Content-Types bypassing validation ([GHSA-573f-x89g-hqp9](https://github.com/fastify/fastify/security/advisories/GHSA-573f-x89g-hqp9))
