# Update May 2025

This report summarizes the accomplishments made during May 2025 within the Node.js project, spanning security releases, automation improvements, governance activities, and security working group efforts.

## Node.js

### Node.js 24 Release

On **May 6, 2025**, Node.js v24.0.0 was officially released:

* [https://github.com/nodejs/Release/issues/1081](https://github.com/nodejs/Release/issues/1081)

This major version introduced core updates, new features, and breaking changes. Coordination included changelog finalization, release candidate validation, and cross-platform testing.

### Security Releases for Node.js 20, 22, 23, and 24

Security updates were published across multiple active lines:

* [https://nodejs.org/en/blog/vulnerability/may-2025-security-releases](https://nodejs.org/en/blog/vulnerability/may-2025-security-releases)

> This release introduced an update of **llhttp** to the version 9 to Node.js 20 for improved HTTP parsing consistency.

* Resolution of a Windows-specific CVE scope clarification:

  * [https://github.com/nodejs-private/security-release/pull/61](https://github.com/nodejs-private/security-release/pull/61)

### CVE Coordination and Metadata Improvements

The Node.js Security Working Group worked with HackerOne to resolve CVE metadata generation issues affecting recent reports:

* [https://github.com/nodejs/security-wg/issues/1483](https://github.com/nodejs/security-wg/issues/1483)

This collaboration improved consistency in public vulnerability disclosures and supported better CVE tracking for downstream consumers.

### Automation Enhancements in Security Releases

Automation improvements were introduced to reduce manual steps and improve reliability:

* Commit push support with `--sync` in `node-core-utils`:
  * [https://github.com/nodejs/node-core-utils/pull/931](https://github.com/nodejs/node-core-utils/pull/931)
 
* CI green status annotation in security PRs:
  * [https://github.com/nodejs/node-core-utils/pull/932](https://github.com/nodejs/node-core-utils/pull/932)

### Governance Updates

A nomination was submitted to add **panva** to the Node.js Technical Steering Committee (TSC), bringing deeper expertise in authentication standards and ecosystem modules.

### Security Working Group Initiatives

#### CodeQL Optimization for Node.js Core

Static analysis via GitHub CodeQL was refined by excluding non-relevant directories:

* [https://github.com/nodejs/node/pull/58254](https://github.com/nodejs/node/pull/58254)

This reduces noise and improves the relevance of security alerts by ignoring `deps/` and `benchmark/` folders.

#### Security Compliance Checker v1.0

The first release of the **Node.js OpenJS Security Compliance Checker** was finalized:

* [https://github.com/nodejs/security-wg/issues/1440](https://github.com/nodejs/security-wg/issues/1440)

This tool aids maintainers in evaluating their projects against the OpenJS Security Compliance Guide and supports ongoing security maturity assessments.

### Highlighted Talk: Understanding Vulnerabilities in Node.js

At Node Congress 2025, Ulises Gascón presented ["What is a Vulnerability and What's Not?. "](https://gitnation.com/contents/what-is-a-vulnerability-and-whats-not-making-sense-of-nodejs-and-express-threat-models), exploring how threat modeling helps clarify the line between secure code, misconfigurations, and actual vulnerabilities in Node.js and Express. A valuable watch for developers looking to strengthen their security mindset.

