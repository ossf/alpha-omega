# Update June 2025

This report summarizes the accomplishments made during June 2025 within the Node.js project, spanning security enhancements, community engagement, permission model improvements, and ongoing governance initiatives.

## Node.js

### Node.js 24.3.0 Release

Node.js 24.3.0 was successfully released in June 2025, continuing the improvement of the latest major version line with stability enhancements and new features.

### Permission Model Enhancements

Significant improvements were made to the Node.js Permission Model:

* Network Permission Support (SEMVER-MAJOR):
  * [https://github.com/nodejs/node/pull/58517](https://github.com/nodejs/node/pull/58517)
  * Added `--allow-net` permission flag to control network access in Node.js applications

* Implicit File System Read Permission:
  * [https://github.com/nodejs/node/pull/58579](https://github.com/nodejs/node/pull/58579)
  * Improved developer experience by allowing implicit fs reads when the permission model is enabled

* Enhanced Child Process Error Handling:
  * [https://github.com/nodejs/node/pull/58758](https://github.com/nodejs/node/pull/58758)
  * Added `resource` information on child process errors when using the permission model

* Community Education:
  * A video showcasing the permission model was created: [https://www.youtube.com/watch?v=UPgM86AvSmQ](https://www.youtube.com/watch?v=UPgM86AvSmQ)

### Security Initiatives

#### CVE Coordination and Correction

A conflicting CVE that occurred during the last security release was updated to provide correct attribution and an incorrectly issued CVE was dismissed, ensuring accurate vulnerability tracking and proper researcher credit.

#### Private Security Report Resolution

Important fixes were implemented for vulnerabilities reported through HackerOne's private security reporting channel, maintaining the security integrity of the Node.js runtime.

#### Windows Defender Application Control (WDAC) Support

Reviewed implementation of WDAC support for Node.js:
* [https://github.com/nodejs/node/pull/54364](https://github.com/nodejs/node/pull/54364)

This enhancement improves Node.js security posture on Windows environments through better integration with Microsoft's application control policies.

### Dependency Vulnerability Management

Fixed the nodejs-deps-vulnerability-assessment workflow:
* [https://github.com/nodejs/nodejs-dependency-vuln-assessments/issues/202](https://github.com/nodejs/nodejs-dependency-vuln-assessments/issues/202)

This repair ensures proper monitoring of potential vulnerabilities in Node.js dependencies, supporting proactive security management.

### Security Working Group Initiatives

#### Security Code Scanning

Ongoing effort to review security code scanning alerts:
* [https://github.com/nodejs/security-wg/issues/1453](https://github.com/nodejs/security-wg/issues/1453)

This initiative focuses on addressing static analysis findings to improve code quality and reduce potential security issues.

#### OpenJS Security Meeting Participation

Active participation in the OpenJS Security Meeting continued, coordinating security efforts across the foundation's projects and sharing best practices.

### Governance Updates

#### Node.js Release Schedule Discussion

Ongoing discussion regarding potential changes to the Node.js release schedule:
* [https://github.com/nodejs/Release/issues/953#issuecomment-3006141246](https://github.com/nodejs/Release/issues/953#issuecomment-3006141246)

This conversation aims to optimize release cadence and support periods to better serve the community's needs.

### Community Engagement

#### LogRocket Podcast on Node.js 24

Participated in a LogRocket podcast discussing Node.js 24, its new features, performance improvements, and the roadmap for future development.

#### Weekly Live Streams on Node.js Contribution

Launched regular Friday live streams teaching community members how to contribute to Node.js, with special focus on security contributions, lowering the barrier to entry for new contributors.

### Reporting and Documentation

#### Mid-year Alpha Omega Report

Published a comprehensive blog post summarizing all Alpha Omega work accomplished during the first half of 2025, highlighting security improvements, vulnerability management, and community education initiatives.