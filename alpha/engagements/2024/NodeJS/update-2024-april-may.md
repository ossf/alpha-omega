# Update April-May 2024

The following update is according to the [Security Support Role](./security-support-role.md) document.

Each section points to at least one item on the priority list defined by the Security Support Role document.

## 1) Fix and Triage Security Issues

* 34 reports were submitted during March 15 to May 31.
  * 3 New
  * 3 Triaged
  * 4 Duplicated
  * 4 Non applicable
  * 1 Spam
  * 19 Informative

* nodejs-cve-checker is now part of Node.js organization

## 2) Support for Security Releases

* Two security releases
  * April 3 - HTTP/2 & HTTP/1.1 fixes (High and Medium severity respectively)
    * Anna Heignssen helped on HTTP/2 resolution (https://github.com/nodejs-private/node-private/pull/561)
  * April 10 - Fixing Windows BadBatBug (High severity)
  * Coordinated via MITRE with other platforms (Rust, PHP, ...)

* Node.js 22 release (team effort - Rafael and Marco Ippolito)

* Some updates to the release workflow were made
  * Mention `export GPG=$(TTY)` to show password UI when signing keys
  * Disable `--follow-tags` by default to avoid pushing "Working on" commit with the tag

* Onboard Marco Ippolito to the Releasers team

## 3) Node.js Security Team Initiatives

* The initiatives for 2024 were defined! https://github.com/nodejs/security-wg/issues/1255

> Selected Initiatives for 2024:
>
> * 1) Automate Security release process - Champion: @RafaelGSS / @marco-ippolito
> * 2) Node.js maintainers: Threat Model - Champion: @nodejs/security-wg
> * 4) Audit build process for dependencies - Champion: @mhdawson 
>
> Please note we have skipped item 3 (SBOM) as we don't have a volunteer for that.

* Microsoft joined Node.js Security Team meeting to discuss a replacement to `--policy-integrity` and
compromising on supporting an eventual feature https://github.com/nodejs/security-wg/blob/main/meetings/2024-04-25.md

* Permission Model
  * [notable] Throw Async Errors on Async APIs https://github.com/nodejs/node/pull/52730
  * [notable] use node::PathResolve and remove known limitation https://github.com/nodejs/node/pull/52761
  * Update documentation to mention fd aren't supported while working with Permission Model https://github.com/nodejs/node/pull/53125
  * [semver-minor] Add `--allow-wasi` support to permission model https://github.com/nodejs/node/pull/53124
  * Add `process.chdir` support to permission model https://github.com/nodejs/node/pull/53175
  * Permission Model flagged as "completed" by Node.js Security Team https://github.com/nodejs/security-wg/pull/1301

* Disable `NODE_REPL_EXTERNAL_MODULE` when `kDisableNodeOptions` is active https://github.com/nodejs/node/pull/52905

* Remove `--experimental-policy` entirely
  * https://github.com/nodejs/node/pull/52583
  * https://github.com/nodejs/node/pull/52602

* Add Undefined Behavior Sanitizer to Node.js - https://github.com/nodejs/node/pull/46297
  * Temporary disabled in https://github.com/nodejs/node/pull/52560
  * Attempt to enable it again in https://github.com/nodejs/node/pull/53142

* Several updates to `node-core-utils` to the Security Release automation

* Release of `is-my-node-vulnerable@1.4.1`

* Meeting with OSTIF to provide feedback

## 4) Node.js Security Sustainability

* Active work on `#nodejs-mentoring` and live streams

## 5) Improving Security Processes

* Latest CITGM module status https://github.com/nodejs/citgm/issues/1060
