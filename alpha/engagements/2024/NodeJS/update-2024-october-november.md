# Update October-November 2024

This report summarizes the accomplishments made during October and November 2024
within the Node.js project, spanning security initiatives, automation,
community engagements, and release processes.

## Summary

The last two months have been highly productive, with important progress in the release automation,
community engagement, and important release policies.
This period also included the release of Node.js 23.0.0.

### Security Release

We processed 10 security reports in total: 1 spam, 4 non-applicable, 2 informative, 2 new issues,
and 1 triaged. Improvements to our security release workflow were also achieved.
The `git node release --pre-announcement` command [now updates the website banner and set the location
of the blog post](https://github.com/nodejs/node-core-utils/pull/874). Additionally, CVE-ID commit metadata
is now automatically included in changelogs, improving the speed of generating security release proposals.
To archive this, three PRs were created:

* One to update our documentation https://github.com/nodejs/node/pull/55830
* One to update `changelog-maker` - The tool Node.js uses to generate release changelogs - https://github.com/nodejs/changelog-maker/pull/167
* and one to update `commit-stream` - One of `changelog-maker` dependencies - https://github.com/nodejs/commit-stream/pull/15

### Releases

The alpha-omega sponsored the released of [Node.js 23.0.0 (semver-major)](https://nodejs.org/en/blog/release/v23.0.0)
and 22.3.0. Additionally, [a FAQ section has been created](https://github.com/nodejs/node/pull/55992) into the releases.md file as an attempt to help relesers during
a release promotion.

An important change has dropped into Node.js major releases policy. From Node.js 24 onwards, one month of
preparation and testing will be required, which means, no commits will land into a major-release without
a baking time of 1 month. This change should allow maintainers to test out canary releases and we ensure
Node.js is releasing a stable major version. For more context, see: https://github.com/nodejs/Release/issues/1054.

### Automation of Node.js Releases

The last two months were rich in improvements to our release automation. An important
millestone has been reached: Node.js could create [a release proposal](https://github.com/nodejs/node/pull/56040) fully automated!
This is a very important step aiming an automated release process.

To archive this, several PRs had to land over the last 2 months:

* Two new flags has been created to `git node release`
  * `git node release --releaseDate` - https://github.com/nodejs/node-core-utils/pull/863
  * `git node release --yes` - https://github.com/nodejs/node-core-utils/pull/862
* A [new workflow (create-release-proposal)](https://github.com/nodejs/node/pull/55690) has been created
 * [`@nodejs/releasers` has been added as CODEOWNERS](https://github.com/nodejs/node/pull/56043) to guarantee all changes should pass by the team approval
 * Remove defaults targetting `gh workflow run` users https://github.com/nodejs/node/pull/56042
* Roadmap issue: https://github.com/nodejs/Release/issues/1061

> An important work in progress is happening on https://github.com/nodejs/node-core-utils/pull/875

### Community Feedback

We made significant contributions to the Node.js community. The is-my-node-vulnerable tool was announced a
few months ago and we have received a positive feedback from the community.
The tool now supports Node.js versions as early as 0.12 and has been simplified by removing unnecessary
dependencies. This tool is been discussed to be integrated to Node.js core in https://github.com/nodejs/security-wg/issues/852,
however, other actions might be happen meanwhile as:
* Issue a CVE for EOL release lines
* Add a warning to EOL versions of Node.js

We also participated in CityJS Medellin and contributed to the annual Node.js blog post for Alpha Omega

### General Updates

Several other notable updates were made:

* SlowBuffer was runtime deprecated
* Improvements were made to the Permission Model, both in terms of test coverage and user
experience when granting access to specific modules. Reference: https://github.com/nodejs/node/pull/55797
* A new flag, --report-exclude-env, was introduced to allow preservation of environment variables in diagnostic reports.
Reference: https://github.com/nodejs/node/pull/55697
