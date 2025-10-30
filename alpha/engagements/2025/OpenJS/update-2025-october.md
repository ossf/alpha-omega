# Update October 2025

This report summarizes the accomplishments made during October 2025 within the OpenJS Ecosystem and Node.js project, spanning security initiatives, community engagement, project coordination, and release engineering.

## OpenJS Ecosystem

### Security and Governance Initiatives

* Led community discussions on **npm Trusted Publishing** security implications and proposed mitigations for critical risks.
  * Initial meeting held by the OpenJS Security Collab Space: [openjs-foundation/security-collab-space#296](https://github.com/openjs-foundation/security-collab-space/pull/296)  
  * Outcome documented and discussed publicly: [community/discussions/178140](https://github.com/orgs/community/discussions/178140)

### Community and Collaboration

* Participated in the **Node.js Collaborator Summit**:
  * Contributed to discussions on the **next Node.js release schedule**: [nodejs/lts-schedule#29](https://github.com/nodejs/lts-schedule/pull/29)
  * Joined the **joint Node.js and Express security session**, covering incident coordination and secure dependency management: [openjs-foundation/summit#464](https://github.com/openjs-foundation/summit/issues/464)
  * Notes and outcomes will be published and merged into the PR in November.
* Recorded an interview for **Software Engineering Daily** covering Node.js performance, security, and ecosystem sustainability (episode pending release).
* Lodash has improved its security posture by following the example of Express and Webpack and adopting a [Threat Model](https://github.com/lodash/lodash/pull/6026) and an [Incident Response Plan (IRP)](https://github.com/lodash/lodash/pull/6028).
* Prepared a blog post titled *“Rethinking Security: From Bugs to Threat Models”*, which explains how maintainers can adopt threat models. It will be published in early November as part of a series of blog posts promoting best practices across the JS ecosystem beyond the projects within the OpenJS Foundation.

## Node.js

### Security Enhancements

* **Backported `--allow-inspector`** to the v24.x line to enhance the Permission Model in LTS releases: [nodejs/node#60248](https://github.com/nodejs/node/pull/60248)
* Continued triaging **HackerOne** reports and coordinating ecosystem-level responses.

* Reviewed multiple **HackerOne vulnerability reports**, ensuring timely triage and coordinated disclosure processes.

* Reviewed the latest **OpenSSL Security Release** to assess its potential impact on Node.js and dependent projects: [nodejs-dependency-vuln-assessments#213](https://github.com/nodejs/nodejs-dependency-vuln-assessments/issues/213)

* Fixed issues in **nodejs-dependency-vuln-assessment** to restore report generation and accuracy: [nodejs-dependency-vuln-assessments#214](https://github.com/nodejs/nodejs-dependency-vuln-assessments/pull/214)

### Runtime and Feature Improvements

* **Added `cooldown` property for Dependabot** to improve automation control and prevent redundant dependency update PRs:
  [nodejs/node#59978](https://github.com/nodejs/node/pull/59978) (part of [nodejs/node#59911](https://github.com/nodejs/node/issues/59911))
* **Released Node.js v24.10.0**, the last minor release in the 24.x line, containing minor improvements and quality-of-life changes:
  [nodejs/node/releases/tag/v24.10.0](https://github.com/nodejs/node/releases/tag/v24.10.0)
* **Released Node.js v25.0.0 (Major)** — focusing on secure-by-default apps, web standards, and runtime modernization:
  * Added `--allow-net` to the Permission Model
  * Exposed global `ErrorEvent`
  * Enabled Web Storage by default
  * Upgraded V8 to **14.1**
    [nodejs/node/releases/tag/v25.0.0](https://github.com/nodejs/node/releases/tag/v25.0.0)
* **Small DX improvement:** added `--markdown` flag for generating simplified major version listings:
  [nodejs/node#60179](https://github.com/nodejs/node/pull/60179)
