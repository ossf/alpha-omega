# Update August-September 2024

The following update is according to the [Security Support Role](./security-support-role.md) document.

Each section points to at least one item on the priority list defined by the Security Support Role document.

## 1) Fix and Triage Security Issues

* 7 reports were submitted during August 1st to September 30.
  * 1 New
  * 1 Triaged
  * 1 Non applicable
  * 2 Informative
  * 2 Spam

## 2) Support & Automation of Security Releases

* Node.js 22.6.0
* Node.js 22.7.0
* Node.js 22.8.0
* Node.js 22.9.0

* Add git node security --cleanup
  * https://github.com/nodejs/node-core-utils/pull/833
  * https://github.com/RafaelGSS/node-core-utils/pull/1
  * https://github.com/nodejs-private/security-release/issues/20
  * https://github.com/nodejs/node/pull/54381

* Handle H1 errors when fetching triaged reports
  * https://github.com/nodejs/node-core-utils/pull/858

* Review IBB mail from last security release

* CITGM
  * Add warn when module is failing on all platforms - https://github.com/nodejs/node-core-utils/pull/843
  * Fix `cheerio` test command - https://github.com/nodejs/citgm/pull/1071
  * Fix `jest` and `mime` errors - https://github.com/nodejs/citgm/pull/1063 (collaboration with maintainers)

* Ping `#node-core` on review-wanted PRs
  * https://github.com/nodejs/node/pull/55102

* Fixed recent unpublished CVEs
  * https://github.com/nodejs/nodejs-cve-checker/issues?q=is%3Aissue+is%3Aclosed

## 3) Node.js Security Team Initiatives

* Node.js Maintainers table
  * https://github.com/nodejs/TSC/issues/1618
  * @nodejs/releasers health - https://github.com/nodejs/Release/issues/1036

* Permission Model
  * Support Buffer on `permission.has` - https://github.com/nodejs/node/pull/54104
  * Update documentation to note `node:fs` on Permission Model section - https://github.com/nodejs/node/pull/54269
  * Add Security Team as CODEOWNERS of test-permission-* - https://github.com/nodejs/node/pull/54267
  * Add resource to internal module stat test - https://github.com/nodejs/node/pull/55157
  * Update documentation to mention more `--allow-*` flags - https://github.com/nodejs/node/pull/55166

* Policy
  * Remove `--experimental-policy` documentation - https://github.com/nodejs/node/pull/54266

* Add alert to REPL usage on TCP
  * https://github.com/nodejs/node/pull/54594

* Cleanup @nodejs/security-wg repository
  * https://github.com/nodejs/security-wg/pull/1387

* Support _severity_ on Node.js Vulnerability Database and on `is-my-node-vulnerable`
  * https://github.com/nodejs/security-wg/pull/1374
  * https://github.com/RafaelGSS/is-my-node-vulnerable/releases/tag/v1.5.0

* Windows Policy-Integrity
  * https://github.com/nodejs/node/pull/54364
  * Microsoft developers joined Security Team meetings to discuss possibility to include a policy-integrity feature to Node.js
    * Initially, Windows only. However, Mickaël Salaün (Microsoft) is working on a Linux support and recently
    joined Security Team call to show the status quo and how we could implement it on Node.js - https://lwn.net/Articles/982085/ 
  * Microsoft also offered help in case of security vulnerabilities to this specific feature
  * Last meeting https://github.com/nodejs/security-wg/pull/1386

* Support to NO_COLORS on `util.styleText` - https://github.com/nodejs/node/pull/54389
  * _This might not be related to security at all_

## 4) Node.js Security Sustainability

* Node.js Security Automated process got mentioned in the Socket.dev blog post
  * https://socket.dev/blog/node-js-doubles-security-releases-with-newly-automated-process
  * This was also amplified by NodeWeekly newsletter

* Rafael delivered two workshops at Grace Hopper Celebration Day on "How to contribute to Node.js Security"

* Rafael will participate at CityJS Medellin to talk about Node.js Permission Model

* Rafael will participate at NodeConf EU to talk about Performance and join
the Node.js Collab Summit to discuss security

* Rafael is working on Node.js 23 release
