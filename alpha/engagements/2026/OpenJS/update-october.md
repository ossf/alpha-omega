# OpenJS Foundation Security Update: October 2026

*Covering October 2026 | Powered by the Alpha-Omega Partnership*

This month's work focused on Node.js permission model fixes, security release preparation, and Alpha release infrastructure, release documentation, and security triage. Below is a summary of completed items across Node.js core, release tooling, security release support, and documentation.

## Node.js Permission Model & Security Fixes

Permission model work continued across filesystem grants, audit mode, environment permissions, VFS behavior, and documentation.

- **Investigate potential same-file duplicated tests on test-permission-\***: Investigated potential same-file duplicated tests on `test-permission-*` in Node.js.
  - [PR #66450](https://github.com/nodejs/node/pull/66450) (Completed Oct 3)
- **child_process: propagate config-file permissions to child processes**: Propagated config-file permissions to child processes.
  - [PR #66559](https://github.com/nodejs/node/pull/66559) (Completed Oct 8)
- **doc: document URL and Uint8Array references in process.permission**: Documented URL and Uint8Array references in `process.permission`.
  - [PR #66557](https://github.com/nodejs/node/pull/66557) (Completed Oct 8)
- **doc: list --allow-inspector and --allow-openssl-store in audit mode**: Listed `--allow-inspector` and `--allow-openssl-store` in permission audit mode. (Completed Oct 9)
- **lib: add --allow-fs-vfs to permission available flags**: Added `--allow-fs-vfs` to the permission available flags.
  - [PR #66554](https://github.com/nodejs/node/pull/66554) (Completed Oct 10)
- **src: release uv_fs_t in permission WildcardIfDir for directories**: Released `uv_fs_t` in permission `WildcardIfDir` for directories.
  - [PR #66555](https://github.com/nodejs/node/pull/66555) (Completed Oct 13)
- **permission: keep explicit fs grants when dropping a covering directory**: Kept explicit filesystem grants when dropping a covering directory.
  - [PR #66556](https://github.com/nodejs/node/pull/66556) (Completed Oct 13)
- **doc: list openssl-store channel and drop field in permissions**: Listed the OpenSSL STORE channel and `drop` field in the permissions documentation.
  - [PR #66558](https://github.com/nodejs/node/pull/66558) (Completed Oct 13)
- **doc: list futimes among fd APIs disabled by the permission model**: Listed `futimes` among file descriptor APIs disabled by the permission model.
  - [PR #66649](https://github.com/nodejs/node/pull/66649) (Completed Oct 13)
- **vfs: allow mounting in permission audit mode**: Allowed VFS mounting in permission audit mode.
  - [PR #66745](https://github.com/nodejs/node/pull/66745) (Completed Oct 15)
- **permission: do not grant cwd read access when there is no entrypoint**: Avoided granting cwd read access when there is no entrypoint.
  - [PR #66645](https://github.com/nodejs/node/pull/66645) (Completed Oct 20)
- **permission: revoke prefix grants when dropping an env pattern**: Revoked prefix grants when dropping an environment permission pattern.
  - [PR #66773](https://github.com/nodejs/node/pull/66773) (Completed Oct 22)
- **doc: document --allow-fs-vfs in the permission model page**: Documented `--allow-fs-vfs` in the permission model page.
  - [PR #66793](https://github.com/nodejs/node/pull/66793) (Completed Oct 23)

## Security Release Support & Triage

Security release work included release post updates, vulnerability checking tests, and triage follow-up.

- **Upcoming Node.js security release preparation**: The upcoming Node.js security release was prepared. (Completed Oct 16)
- **Blog: announce october 2026 security release**: Announced the October 2026 security release on the Node.js website.
  - [nodejs/nodejs.org#9217](https://github.com/nodejs/nodejs.org/pull/9217) (Completed Oct 16)
- **Blog: add CVE summaries to oct 2026 sec release post**: Added CVE summaries to the October 2026 security release post.
  - [nodejs/nodejs.org#9234](https://github.com/nodejs/nodejs.org/pull/9234) (Completed Oct 23)
- **test: add october 2026 security release tests**: Added October 2026 security release tests to `is-my-node-vulnerable`.
  - [nodejs/is-my-node-vulnerable#39](https://github.com/nodejs/is-my-node-vulnerable/pull/39) (Completed Oct 29)
- **Investigation of is-my-node-vulnerable on Node.js 24.22.0**: Investigated whether `is-my-node-vulnerable` should recognize Node.js v24.22.0 as vulnerable according to the October 2026 security release. (Completed Oct 28)
- **Review of article on legitimate node.exe used for detection evasion**: Analyzed an article about attackers using the legitimate signed `node.exe` to execute malicious JavaScript and noted it is not a Node.js Core vulnerability.
  - [PR #66530](https://github.com/nodejs/node/pull/66530) (Completed Oct 7)
- **Review of HackerOne report 4094553**: Reviewed whether HackerOne report 4094553 should be reopened and whether PR #64393 covered the reported security fix. (Completed Oct 23)
- **doc: add rafael and antoine as last security release stewards**: Added Rafael and Antoine as last security release stewards.
  - [PR #66909](https://github.com/nodejs/node/pull/66909) (Completed Oct 23)
- **Private repository PR access**: Granted access related to opening PRs in a private repository.
  - [nodejs/admin#1101](https://github.com/nodejs/admin/issues/1101) (Completed Oct 3)
  - 
## Release Pipeline & Alpha Release Support

Release tooling was updated for Alpha release support across Node.js repositories and related infrastructure.

- **doc: update V8 ABI release policy**: Updated the V8 ABI release policy.
  - [PR #64196](https://github.com/nodejs/node/pull/64196) (Completed Oct 1)
- **Review and adjustment of nodejs/node#64196**: Reviewed nodejs/node#64196 and applied review suggestions in a fixup commit.
  - [PR #64196](https://github.com/nodejs/node/pull/64196) (Completed Oct 19)
- **[v22.x] deps: update sqlite to 3.53.4**: Updated sqlite to 3.53.4 on v22.x.
  - [PR #66246](https://github.com/nodejs/node/pull/66246) (Completed Oct 18)
- **feat: accept alpha versions in YAML comments**: Accepted alpha versions in YAML comments.
  - [nodejs/remark-preset-lint-node#729](https://github.com/nodejs/remark-preset-lint-node/pull/729) (Completed Oct 17)
- **fix: recognise alpha release commits**: Recognized alpha release commits.
  - [nodejs/changelog-maker#279](https://github.com/nodejs/changelog-maker/pull/279) (Completed Oct 20)
- **build: add expected assets for v27.x**: Added expected assets for v27.x.
  - [nodejs/build#4522](https://github.com/nodejs/build/pull/4522) (Completed Oct 21)
- **doc: document the Alpha phase and v27 schedule**: Documented the Alpha phase and v27 schedule.
  - [nodejs/Release#1188](https://github.com/nodejs/Release/pull/1188) (Completed Oct 21)
- **feat: support the Alpha release phase**: Added support for the Alpha release phase on the Node.js website.
  - [nodejs/nodejs.org#9223](https://github.com/nodejs/nodejs.org/pull/9223) (Completed Oct 22)
- **build,doc,tools: support alpha releases**: Added build, documentation, and tooling support for alpha releases.
  - [PR #66796](https://github.com/nodejs/node/pull/66796) (Completed Oct 26)
- **feat: support alpha versions**: Added support for alpha versions in `nodejs-dist-indexer`.
  - [nodejs/nodejs-dist-indexer#107](https://github.com/nodejs/nodejs-dist-indexer/pull/107) (Completed Oct 27)
- **feat(release): support alpha releases**: Added release support for alpha releases in `node-core-utils`.
  - [nodejs/node-core-utils#1224](https://github.com/nodejs/node-core-utils/pull/1224) (Completed Oct 28)
- **doc: note linear history rule on branch-off**: Documented the linear history rule on branch-off.
  - [PR #67057](https://github.com/nodejs/node/pull/67057) (Completed Oct 29)
- **deps: patch npm engines to accept alpha versions**: Patched npm engines to accept alpha versions.
  - [PR #67063](https://github.com/nodejs/node/pull/67063) (Completed Oct 29)
- **2026-10-28, Version 27.0.0-alpha.0.0.0 (Alpha)**: Prepared the Node.js 27.0.0 Alpha release proposal.
  - [PR #67062](https://github.com/nodejs/node/pull/67062) (Completed Oct 29)
- **tools: lint first Alpha release proposals**: Added linting for first Alpha release proposals.
  - [PR #67065](https://github.com/nodejs/node/pull/67065) (Completed Oct 30)

## Documentation & Reporting

## In Progress

The following work remained open at the end of the month.

- **permission: enforce when both --permission and --permission-audit are set**: Enforces the permission model when both `--permission` and `--permission-audit` are set.
  - [PR #67036](https://github.com/nodejs/node/pull/67036) (Awaiting CI)
- **doc: describe how the permission model grants the entrypoint**: Describes how the permission model grants the entrypoint.
  - [PR #67038](https://github.com/nodejs/node/pull/67038) (Awaiting CI)
- **src,permission: reject async mkdir, rmdir, chmod, readlink and utimes asynchronously**: Rejects async `mkdir`, `rmdir`, `chmod`, `readlink`, and `utimes` asynchronously under the permission model.
  - [PR #67037](https://github.com/nodejs/node/pull/67037) (Awaiting CI)
- **fs: suggest --allow-fs-read in lstat permission errors**: Suggests `--allow-fs-read` in `lstat` permission errors.
  - [PR #66969](https://github.com/nodejs/node/pull/66969) (Awaiting CI)
- **permission: match directory grants when dropping a path whose type changed**: Matches directory grants when dropping a path whose type changed.
  - [PR #66766](https://github.com/nodejs/node/pull/66766) (Awaiting CI)
- **permission: reject an empty reference in permission.drop()**: Rejects an empty reference in `permission.drop()`.
  - [PR #66732](https://github.com/nodejs/node/pull/66732) (Awaiting CI)
- **fs: do not disable fd-based APIs in permission audit mode**: Avoids disabling fd-based filesystem APIs in permission audit mode.
  - [PR #66726](https://github.com/nodejs/node/pull/66726) (Awaiting CI)
- **child_process: copy list permission flags from option values**: Copies list permission flags from option values for child processes.
  - [PR #66725](https://github.com/nodejs/node/pull/66725) (Awaiting CI)
- **path: avoid building error label per argument in posix.resolve**: Avoids building an error label per argument in `posix.resolve`.
  - [PR #66616](https://github.com/nodejs/node/pull/66616) (Awaiting CI)
- **nsolid with --permission-audit enabled by default**: Adds a way for nsolid to listen to `--permission-audit` errors and send them to its console.
  - [nodesource/nsolid#562](https://github.com/nodesource/nsolid/pull/562) (Awaiting CI)
- **nodejs-core: ground test, error, semver and benchmark rules in review**: Grounds Node.js core test, error, semver, and benchmark rules in review.
  - [mcollina/skills#41](https://github.com/mcollina/skills/pull/41) (Awaiting CI)
- **Review of nodejs/node#66929**: Review of nodejs/node#66929 is in progress. (In progress)
- **Investigate and fix hang in relaxed httpValidation**: Investigation and correction of a hang in relaxed `httpValidation` is in progress. (In progress)
