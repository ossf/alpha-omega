## Omega

The purpose of Omega is to run leading-edge security analysis against the top 10,000 (or more)
open source projects, to validate and triage those findings, and then to get the issues fixed
by working with project maintainers.

### Omega is Hiring!

We're currently hiring a security researcher:

* [Security Researcher/Analysis](https://linuxfoundation.org/JobPosting/?743999811940036) -
  Primary responsibility is to identify and fix new vulnerabilities across the open source ecosystem.

This role will work closely with our core team to meaningfully improve the security of the open
source software we all depend on every day.

If you, or anyone you know may be interested in one of this role, please have them apply using
the links above.

### Analysis Toolchain

Omega uses a publicly available toolchain, which consists of dozens of open source and freely-
available tools. These tools include CodeQL, Semgrep, OSS Gadget, and others. For a full list
of analyzers, please see [list-of-tools](analyzer/list-of-tools.md).

To run the Omega analysis toolchain, please see [analyzer](analyzer/README.md).

### Omega Assertion Framework

Omega provides a set of tools for generating assertions and executing policies against them.
For more information, see [OAF](oaf/README.md).