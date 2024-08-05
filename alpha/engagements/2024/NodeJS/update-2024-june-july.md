# Update June-July 2024

The following update is according to the [Security Support Role](./security-support-role.md) document.

Each section points to at least one item on the priority list defined by the Security Support Role document.

> Two meetings to discuss the Security Support Role document happened during June/July.
> * https://github.com/ossf/alpha-omega/pull/386

## 1) Fix and Triage Security Issues

* 20 reports were submitted during June 1st to July 31.
  * 1 New
  * 1 Resolved
  * 2 Triaged
  * 3 Duplicated
  * 8 Non applicable
  * 5 Informative

## 2) Support & Automation of Security Releases

* One security release
  * CVE-2024-36138 - Bypass incomplete fix of CVE-2024-27980 (High)
  * CVE-2024-22020 - Bypass network import restriction via data URL (Medium)
  * CVE-2024-22018 - fs.lstat bypasses permission model (Low)
  * CVE-2024-36137 - fs.fchown/fchmod bypasses permission model (Low)
  * CVE-2024-37372 - Permission model improperly processes UNC paths (Low)

* Node.js 22.5.0
* Node.js 22.3.0

* Support to trailing slash on PR-URL Metadata
  * https://github.com/nodejs/branch-diff/pull/70
  * https://github.com/nodejs/branch-diff/pull/72
* Added test CI for nodejs-private/security-release
* Fetch PR_URL from HackerOne
  * https://github.com/nodejs/node-core-utils/pull/815
* Mention EOL in Node.js security release template
  * https://github.com/nodejs/node-core-utils/pull/816
* Add test case for CVSS on nodejs-private/security-release
* Sort verions ASC on security release blog post
  * https://github.com/nodejs/node-core-utils/pull/831
* Add git node security --sync
  * https://github.com/nodejs/node-core-utils/pull/818
* Update Node.js security-release-process document to automated one
  * https://github.com/nodejs/node-core-utils/pull/832
  * https://github.com/nodejs/node/pull/53877
* Update RafaelGSS releasers key
  * https://github.com/nodejs/release-keys/issues/29
  
## 3) Node.js Security Team Initiatives

* Permission Model
  * How wildcard works https://github.com/nodejs/node/issues/53621
  * https://github.com/nodejs/node/pull/53664
  * Mention V8.setFlagsFromString API https://github.com/nodejs/node/pull/53731
  * Remove path.resolve https://github.com/nodejs/node/pull/53729
  
* Policy for Experimental Features discussion
  * https://github.com/nodejs-private/node-private/issues/601
  * Further discussion will be handled by Next-10 group
  
* Drop --experimental-network-imports
  * https://github.com/nodejs/node/pull/53822
  
* OSSF Monitor is now part of OpenSSF
  * https://github.com/ossf/scorecard-monitor/issues/79
