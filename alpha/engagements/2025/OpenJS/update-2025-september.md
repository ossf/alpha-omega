# Update September 2025

This report summarizes the accomplishments made during September 2025 within the OpenJS Ecosystem and Node.js project, spanning security initiatives, community engagement, project coordination, and release engineering.

## OpenJS Ecosystem

### Security and Governance Initiatives

* Published blog post announcing the Alpha-Omega initiative: [Security Support for OpenJS Projects](https://openjsf.org/blog/security-support-for-openjs-projects)
* Released the first version of **OpenJS Monitor** to track vulnerabilities across ecosystem projects: [openjs-monitor](https://github.com/RafaelGSS/openjs-monitor)
* Defined minimal `SECURITY.md` requirements for all OpenJS Projects: [openjs-foundation/cross-project-council#1588](https://github.com/openjs-foundation/cross-project-council/pull/1588)
    * Created dozens of PRs to update (and in some cases create) `SECURITY.md` files across the foundation projects to include the CNA Escalation policy
* Created Incident Response Plans (IRPs) for several projects:
  * Webpack – [webpack/webpack#19841](https://github.com/webpack/webpack/pull/19841)
  * WebDriverIO – (under review)
  * NativeScript – (under review)
  * MessageFormat – (under review)
* Created Threat Model for Webpack (https://github.com/webpack/security-wg/pull/9)
* Enhanced OpenJS Monitor by integrating more packages to broaden vulnerability coverage: [openjs-foundation/command-center#91](https://github.com/openjs-foundation/command-center/pull/91)

### Project Support

* Continued work with **NativeScript**, replacing packages with Node.js built-ins to reduce supply chain exposure: [nativescript-cli#5853](https://github.com/NativeScript/nativescript-cli/pull/5853) and helping adopting OSSF scorecard best practices
* Continued work with **Express** to launch a Bug Bounty program in the YesWeHack plantform (under review): https://github.com/expressjs/security-wg/pull/90
* Helping with security onboarding for new Foudnation projects: Lit, Perspective and GeoDa.AI

## Node.js

### Security Enhancements

* Created **Node.js Web Infra Incident Response Plan**: [nodejs/web-team#44](https://github.com/nodejs/web-team/pull/44)
* Added `SECURITY.md` to core Node.js websites:

  * Node.js.org – [nodejs/nodejs.org#8171](https://github.com/nodejs/nodejs.org/pull/8171)
  * Node.js Web Infra – [nodejs/web-team#44](https://github.com/nodejs/web-team/pull/44)
* Held an **“emergency” security incident meeting with npm** to improve coordination and response: [nodejs/security-wg#1524](https://github.com/nodejs/security-wg/pull/1524)
* Improved Node.js security release automation by adding comments on builds and docker cleanup tasks: [node-core-utils#973](https://github.com/nodejs/node-core-utils/pull/973)

### Runtime and Feature Improvements

* Stabilized `--disable-sigusr1`: [nodejs/node#59707](https://github.com/nodejs/node/pull/59707)
* Introduced `--allow-inspector` to the Permission Model: [nodejs/node#59711](https://github.com/nodejs/node/pull/59711)
* Backported UNC patch to Node.js 22: [nodejs/node#59831](https://github.com/nodejs/node/pull/59831)
